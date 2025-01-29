<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

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
    echo 'Exception when calling Store#placeOrder: '
        . print_r($e->getResponseObject());
}
