<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

use PrestaShop\PrestaShop\Adapter\Entity\StockAvailable;
use PrestaShop\PrestaShop\Adapter\Entity\Product; // Jeśli chcesz dodatkowo dezaktywować produkt

require_once dirname(__FILE__) . '/../config/config.inc.php';
require_once dirname(__FILE__) . '/../init.php';

// Lista ID produktów do dezaktywacji / ustawienia jako niedostępne
$products_to_disable = [2204];

foreach ($products_to_disable as $id_product) {
    $id_product_attribute = 0; // Jeśli brak kombinacji – zostaje 0

    // 1. Ustaw ilość magazynową na 0
    StockAvailable::setQuantity($id_product, $id_product_attribute, 0);

    // 2. Nie pozwalaj zamawiać przy braku stanu magazynowego
    // Wartości:
    // 0 = nie pozwól zamawiać
    // 1 = pozwól zamawiać
    // 2 = użyj ustawień globalnych
    StockAvailable::setProductOutOfStock($id_product, 0, $id_product_attribute);

    echo "Produkt $id_product ustawiony jako niedostępny.\n";
}
