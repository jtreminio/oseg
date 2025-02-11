<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

try {
    $response = (new OpenAPI\Client\Api\PetApi(config: $config))->uploadFile(
        pet_id: 12345,
        additional_metadata: "Additional data to pass to server",
        file: new SplFileObject("/path/to/file"),
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Pet#uploadFile: {$e->getMessage()}";
}
