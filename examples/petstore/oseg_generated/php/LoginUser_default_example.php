<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\UserApi($config))->loginUser(
        username: "my_username",
        password: "my_secret_password",
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#loginUser: '
        . print_r($e->getResponseObject());
}
