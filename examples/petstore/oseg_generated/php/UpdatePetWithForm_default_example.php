<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\PetApi(config: $config))->updatePetWithForm(
        pet_id: 12345,
        name: "Pet's new name",
        status: "sold",
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#updatePetWithForm: '
        . print_r($e->getResponseObject());
}
