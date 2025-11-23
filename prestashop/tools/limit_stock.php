<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

use PrestaShop\PrestaShop\Adapter\Entity\Product;
use PrestaShop\PrestaShop\Adapter\Entity\StockAvailable;

require_once dirname(__FILE__) . '/../config/config.inc.php';
require_once dirname(__FILE__) . '/../init.php';

$max_quantity = 10;

// Pobranie wszystkich produktów w sklepie
$all_products = Product::getProducts(
    (int) Context::getContext()->language->id,
    0,
    0,
    'id_product',
    'ASC'
);

StockAvailable::setQuantity(2204, 0, $max_quantity);
echo "Produkt 2204: ilość zmniejszona z 100 do $max_quantity.\n";

