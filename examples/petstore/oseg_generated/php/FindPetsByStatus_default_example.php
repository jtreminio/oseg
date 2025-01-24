<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\PetApi($config))->findPetsByStatus(
        status: [
            OpenAPI\Client\Model::STATUS_AVAILABLE,
            OpenAPI\Client\Model::STATUS_PENDING,
        ],
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#findPetsByStatus: '
        . print_r($e->getResponseObject());
}
