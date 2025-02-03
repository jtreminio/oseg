<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPI\Client\Api\UserApi(config: $config))->logoutUser();
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling User#logoutUser: {$e->getMessage()}";
}
