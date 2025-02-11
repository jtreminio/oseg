<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");
// $config->setApiKey("api_key", "YOUR_API_KEY");

$order = (new OpenAPI\Client\Model\Order())
    ->setId(12345)
    ->setPetId(98765)
    ->setQuantity(5)
    ->setShipDate(new \DateTime("2025-01-01T17:32:28Z"))
    ->setStatus(OpenAPI\Client\Model\Order::STATUS_APPROVED)
    ->setComplete(false);

try {
    $response = (new OpenAPI\Client\Api\StoreApi(config: $config))->placeOrder(
        order: $order,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Store#placeOrder: {$e->getMessage()}";
}
