<?php
/**
 * Custom settings for this PrestaShop instance.
 *
 * This file is safe to edit and won't be overwritten by upgrades.
 * We define a fallback for SSL cert attachments to emails so that
 * certificates are not attached to customer emails by default.
 */

if (!defined('_PS_SSL_ATTACH_CERT_TO_EMAILS_DEFAULT_')) {
    define('_PS_SSL_ATTACH_CERT_TO_EMAILS_DEFAULT_', 0);
}
