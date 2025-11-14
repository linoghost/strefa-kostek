<?php
use PrestaShop\PrestaShop\Adapter\StockManager;
use PrestaShop\PrestaShop\Adapter\Entity\Product;

require_once dirname(__FILE__) . '/../../config/config.inc.php';
require_once dirname(__FILE__) . '/../../init.php';

$max_quantity = 10;

// Pobranie wszystkich produktów
$all_products = Product::getProducts(
    (int) Context::getContext()->language->id,
    0,
    0,
    'id_product',
    'ASC'
);


foreach ($all_products as $product) {
    $id_product = $product['id_product'];

    // Pobierz aktualną ilość
    $current_quantity = StockManager::getStockAvailable($id_product, 0);

    // Jeśli więcej niż 10, ustaw na 10
    if ($current_quantity > $max_quantity) {
        StockManager::updateQuantity($id_product, 0, $max_quantity);
        echo "Produkt $id_product: ilość zmieniona z $current_quantity na $max_quantity.\n";
    } else {
        echo "Produkt $id_product: ilość ($current_quantity) OK.\n";
    }
}



