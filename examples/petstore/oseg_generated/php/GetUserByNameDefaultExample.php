<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\UserApi(config: $config))->getUserByName(
        username: "my_username",
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#getUserByName: '
        . print_r($e->getResponseObject());
}
