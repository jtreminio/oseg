<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\StoreApi(config: $config);

    $api_caller->deleteOrder(
        order_id: null,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Store#deleteOrder: '
        . print_r($e->getResponseObject());
}
