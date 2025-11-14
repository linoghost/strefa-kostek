<?php
/**
 * CLI helper to generate local CA and server cert for the shop.
 * Usage: php tools/generate_ssl.php example.com
 */
chdir(dirname(__DIR__)); // go to project root
require_once __DIR__ . '/../config/config.inc.php';
require_once __DIR__ . '/../classes/SSLCertificateGenerator.php';

if (php_sapi_name() !== 'cli') {
    echo "This script must be run from CLI.\n";
    exit(1);
}

$domain = $argv[1] ?? null;
if (!$domain) {
    echo "Usage: php tools/generate_ssl.php <domain>\n";
    exit(1);
}

$saveDir = _PS_ROOT_DIR_ . DIRECTORY_SEPARATOR . 'config' . DIRECTORY_SEPARATOR . 'ssl';
try {
    $res = SSLCertificateGenerator::generatePerShopCert($domain, $saveDir);
    echo "Generated files:\n";
    foreach ($res as $k => $v) {
        echo " - $k: $v\n";
    }

    // Save public cert path to configuration so Mail::send can pick it up
    if (class_exists('Configuration')) {
        Configuration::updateValue('PS_SSL_PUBLIC_CERT_PATH', $res['server_cert']);
        Configuration::updateValue('PS_SSL_CA_CERT_PATH', $res['ca_cert']);
        echo "Configuration keys PS_SSL_PUBLIC_CERT_PATH and PS_SSL_CA_CERT_PATH updated.\n";
    } else {
        echo "Warning: Configuration class not available - please set PS_SSL_PUBLIC_CERT_PATH manually.\n";
    }

    echo "IMPORTANT: Do NOT distribute private keys (server.key.pem / ca.key.pem).\n";
    echo "Install the server certificate (server.crt.pem) and server.key.pem on your web server.\n";
    echo "If you want browsers to trust the certificate, import the CA certificate (ca.crt.pem) into client systems.\n";
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage() . "\n";
    exit(1);
}
