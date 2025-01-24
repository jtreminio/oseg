<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\UserApi($config))->loginUser(
        username: null,
        password: null,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#loginUser: '
        . print_r($e->getResponseObject());
}
