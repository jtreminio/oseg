<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\StoreApi(config: $config);

    $response = $api_caller->getOrderById(
        order_id: null,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Store#getOrderById: '
        . print_r($e->getResponseObject());
}
