<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\StoreApi(config: $config))->getOrderById(
        order_id: 3,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Store#getOrderById: '
        . print_r($e->getResponseObject());
}
