<?php
use PrestaShop\PrestaShop\Adapter\Entity\StockAvailable;

require_once dirname(__FILE__) . '/../../config/config.inc.php';
require_once dirname(__FILE__) . '/../../init.php';

// Lista ID produktów, które mają być niedostępne
$products_to_disable = [2204];

foreach ($products_to_disable as $id_product) {

    // Ustaw stan magazynowy na 0
    StockAvailable::setQuantity($id_product, 0, 0);

    // Zablokuj możliwość zakupu brakującego produktu
    StockAvailable::setOutOfStock($id_product, 0);

    echo "Produkt $id_product ustawiony jako niedostępny.\n";
}
