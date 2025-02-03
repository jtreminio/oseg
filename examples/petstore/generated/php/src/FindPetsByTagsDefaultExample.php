<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\PetApi(config: $config))->findPetsByTags(
        tags: [
            "tag_1",
            "tag_2",
        ],
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Pet#findPetsByTags: {$e->getMessage()}";
}
