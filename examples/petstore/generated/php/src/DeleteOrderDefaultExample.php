<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");
// $config->setApiKey("api_key", "YOUR_API_KEY");

try {
    (new OpenAPI\Client\Api\StoreApi(config: $config))->deleteOrder(
        order_id: "12345",
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling Store#deleteOrder: {$e->getMessage()}";
}
