<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPI\Client\Api\PetApi($config))->findPetsByTags(
        tags: [
            "tag_1",
            "tag_2",
        ],
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#findPetsByTags: '
        . print_r($e->getResponseObject());
}
