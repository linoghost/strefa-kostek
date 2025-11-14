<?php
/**
 * Simple SSL/CA generator utility using PHP OpenSSL functions.
 * Produces a local CA (optional) and a server certificate signed by the CA.
 * Saves files to provided directory and DOES NOT distribute private keys by mail.
 */
class SSLCertificateGeneratorCore
{
    /**
     * Generate a local CA and a server certificate for given domain.
     * @param string $domain
     * @param string $saveDir Absolute path where files will be stored (must be writable)
     * @param int $days Validity in days
     * @return array Paths of generated files [ca_cert, server_cert, server_key, ca_key]
     * @throws Exception
     */
    public static function generatePerShopCert(string $domain, string $saveDir, int $days = 3650)
    {
        if (!extension_loaded('openssl')) {
            throw new Exception('OpenSSL PHP extension is required');
        }

        if (!is_dir($saveDir)) {
            if (!mkdir($saveDir, 0750, true)) {
                throw new Exception('Unable to create directory: ' . $saveDir);
            }
        }

        $caKeyConfig = [
            "private_key_bits" => 2048,
            "private_key_type" => OPENSSL_KEYTYPE_RSA,
        ];

        // CA key
        $caKey = openssl_pkey_new($caKeyConfig);
        openssl_pkey_export($caKey, $caKeyPem);

        // CA cert
        $caDn = [
            'countryName' => 'PL',
            'stateOrProvinceName' => 'Unknown',
            'localityName' => 'Unknown',
            'organizationName' => 'Local CA',
            'organizationalUnitName' => 'Local CA',
            'commonName' => 'Local Development CA',
        ];
        $caCsr = openssl_csr_new($caDn, $caKey);
        $caCert = openssl_csr_sign($caCsr, null, $caKey, $days);
        openssl_x509_export($caCert, $caCertPem);

        // Server key
        $serverKey = openssl_pkey_new($caKeyConfig);
        openssl_pkey_export($serverKey, $serverKeyPem);

        // Server CSR
        $serverDn = [
            'countryName' => 'PL',
            'stateOrProvinceName' => 'Unknown',
            'localityName' => 'Unknown',
            'organizationName' => 'Shop',
            'organizationalUnitName' => 'Shop',
            'commonName' => $domain,
        ];

        $san = "DNS:" . $domain;
        $csrConfig = [
            'config' => null,
            'req_extensions' => 'v3_req',
            'private_key_type' => OPENSSL_KEYTYPE_RSA,
        ];

        // Build a temporary openssl config for SAN
        $tmpCfg = tempnam(sys_get_temp_dir(), 'openssl_cnf_');
        $cfg = "[ req ]\ndistinguished_name = req_distinguished_name\nreq_extensions = v3_req\n[ req_distinguished_name ]\n[ v3_req ]\nsubjectAltName = $san\n";
        file_put_contents($tmpCfg, $cfg);

        $csr = openssl_csr_new($serverDn, $serverKey, ['config' => $tmpCfg]);
        // Sign server cert with CA
        $serverCert = openssl_csr_sign($csr, $caCert, $caKey, $days, ['config' => $tmpCfg]);
        openssl_x509_export($serverCert, $serverCertPem);

        // cleanup tmp cfg
        @unlink($tmpCfg);

        // Write files
        $caCertPath = rtrim($saveDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'ca.crt.pem';
        $caKeyPath = rtrim($saveDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'ca.key.pem';
        $serverCertPath = rtrim($saveDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'server.crt.pem';
        $serverKeyPath = rtrim($saveDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'server.key.pem';

        file_put_contents($caCertPath, $caCertPem);
        file_put_contents($caKeyPath, $caKeyPem);
        file_put_contents($serverCertPath, $serverCertPem);
        file_put_contents($serverKeyPath, $serverKeyPem);

        // Set restrictive permissions for private keys
        @chmod($caKeyPath, 0600);
        @chmod($serverKeyPath, 0600);

        return [
            'ca_cert' => $caCertPath,
            'ca_key' => $caKeyPath,
            'server_cert' => $serverCertPath,
            'server_key' => $serverKeyPath,
        ];
    }
}

class_alias('SSLCertificateGeneratorCore', 'SSLCertificateGenerator');
