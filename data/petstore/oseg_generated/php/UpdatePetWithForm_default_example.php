<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\PetApi(config: $config);

    $api_caller->updatePetWithForm(
        pet_id: null,
        name: null,
        status: null,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#updatePetWithForm: '
        . print_r($e->getResponseObject());
}
