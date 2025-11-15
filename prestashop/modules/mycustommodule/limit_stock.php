<?php
use PrestaShop\PrestaShop\Adapter\Entity\Product;
use PrestaShop\PrestaShop\Adapter\Entity\StockAvailable;

require_once dirname(__FILE__) . '/../../config/config.inc.php';
require_once dirname(__FILE__) . '/../../init.php';

$max_quantity = 10;

// Pobranie wszystkich produktów w sklepie
$all_products = Product::getProducts(
    (int) Context::getContext()->language->id,
    0,
    0,
    'id_product',
    'ASC'
);

foreach ($all_products as $product) {
    $id_product = (int) $product['id_product'];

    // Pobierz aktualną ilość produktu
    $current_quantity = StockAvailable::getQuantityAvailableByProduct($id_product);

    // Jeśli więcej niż 10, ustaw na 10
    if ($current_quantity > $max_quantity) {
        StockAvailable::setQuantity($id_product, 0, $max_quantity);
        echo "Produkt $id_product: ilość zmniejszona z $current_quantity do $max_quantity.\n";
    } else {
        echo "Produkt $id_product: ilość OK ($current_quantity).\n";
    }
}
