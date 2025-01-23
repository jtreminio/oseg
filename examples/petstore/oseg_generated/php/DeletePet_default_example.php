<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\PetApi(config: $config);

    $api_caller->deletePet(
        pet_id: null,
        api_key: null,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#deletePet: '
        . print_r($e->getResponseObject());
}
