<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once dirname(__FILE__) . '/../config/config.inc.php';
require_once dirname(__FILE__) . '/../init.php';

// ID produktów, które chcesz wyłączyć
$products_to_disable = [2204, 2203];

foreach ($products_to_disable as $id_product) {
    // Ustaw ilość na 0
    StockAvailable::updateQuantity($id_product, 0, 0);

    // Nie pozwalaj na zakup produktów, które są na 0
    StockAvailable::setProductOutOfStock($id_product, 1);

    echo "Produkt $id_product ustawiony jako niedostępny.<br>";
}
