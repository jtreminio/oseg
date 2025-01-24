<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\StoreApi($config))->deleteOrder(
        order_id: "12345",
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Store#deleteOrder: '
        . print_r($e->getResponseObject());
}
