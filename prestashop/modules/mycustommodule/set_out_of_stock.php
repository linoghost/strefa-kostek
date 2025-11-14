<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
use PrestaShop\PrestaShop\Adapter\StockManager;
use PrestaShop\PrestaShop\Adapter\Entity\Product;

require_once dirname(__FILE__) . '/../../config/config.inc.php';
require_once dirname(__FILE__) . '/../../init.php';

// ID produktów, które mają być niedostępne do kupienia
$products_to_disable = [2204];

foreach ($products_to_disable as $id_product) {
    // Pobranie dostępności produktu
    $stock = StockManager::getStockAvailable($id_product, 0);

    // Ustaw ilość = 0
    StockManager::updateQuantity($id_product, 0, 0);

    // Zablokuj możliwość zamawiania
    StockManager::setProductOutOfStock($id_product, 0);

    echo "Produkt $id_product ustawiony jako niedostępny.\n";
}