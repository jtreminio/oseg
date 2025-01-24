<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\PetApi($config))->deletePet(
        pet_id: null,
        api_key: null,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#deletePet: '
        . print_r($e->getResponseObject());
}
