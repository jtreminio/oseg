<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\PetApi(config: $config))->getPetById(
        pet_id: 12345,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#getPetById: '
        . print_r($e->getResponseObject());
}
