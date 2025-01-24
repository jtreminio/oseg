<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\StoreApi($config))->getInventory();

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Store#getInventory: '
        . print_r($e->getResponseObject());
}
