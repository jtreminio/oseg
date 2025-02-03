<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\StoreApi(config: $config))->deleteOrder(
        order_id: "12345",
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Store#deleteOrder: {$e->getMessage()}";
}
