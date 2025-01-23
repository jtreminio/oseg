<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\UserApi(config: $config);

    $response = $api_caller->getUserByName(
        username: null,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#getUserByName: '
        . print_r($e->getResponseObject());
}
