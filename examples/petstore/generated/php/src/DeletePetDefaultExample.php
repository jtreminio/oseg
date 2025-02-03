<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\PetApi(config: $config))->deletePet(
        pet_id: 12345,
        api_key: "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a",
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Pet#deletePet: {$e->getMessage()}";
}
