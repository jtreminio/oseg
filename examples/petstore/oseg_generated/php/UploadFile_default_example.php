<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPI\Client\Api\PetApi(config: $config);

    $response = $api_caller->uploadFile(
        pet_id: 12345,
        additional_metadata: null,
        file: new SplFileObject("/path/to/file"),
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#uploadFile: '
        . print_r($e->getResponseObject());
}
