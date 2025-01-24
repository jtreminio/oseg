<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\PetApi($config))->uploadFile(
        pet_id: 12345,
        additional_metadata: "Additional data to pass to server",
        file: new SplFileObject("/path/to/file"),
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#uploadFile: '
        . print_r($e->getResponseObject());
}
