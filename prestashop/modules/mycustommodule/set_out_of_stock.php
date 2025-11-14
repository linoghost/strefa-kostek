<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
use PrestaShop\PrestaShop\Adapter\StockManager;

require_once dirname(__FILE__) . '/../../config/config.inc.php';
require_once dirname(__FILE__) . '/../../init.php';

/*
ID produktów które mają być niedostępne:
"niedostępne" = widoczne ale nie mogące być dodane do koszyka
*/
$products_to_disable = [2204];  //jeremi musisz dopisać id bo ja nie wiem skąd je wziąć

/*
metoda `setProductOutOfStock` jest częścią PrestaShop (`StockManager`)
ale działa dopiero w środowisku PrestaShop z poprawnie załadowanym autoloaderem.
 */
foreach ($products_to_disable as $id_product) {
    StockManager::setProductOutOfStock($id_product, 0);
    echo "Produkt $id_product ustawiony jako niedostępny.\n";
}