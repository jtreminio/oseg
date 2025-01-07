<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\UserApi(config: $config);

    $api_caller->deleteUser(
        username: null,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#deleteUser: '
        . print_r($e->getResponseObject());
}
