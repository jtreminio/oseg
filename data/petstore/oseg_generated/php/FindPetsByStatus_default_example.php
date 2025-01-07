<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\PetApi(config: $config);

    $response = $api_caller->findPetsByStatus(
        status: null,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#findPetsByStatus: '
        . print_r($e->getResponseObject());
}
