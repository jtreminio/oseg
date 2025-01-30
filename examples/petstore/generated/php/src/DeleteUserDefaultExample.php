<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

$config = \OpenAPI\Client\Configuration::getDefaultConfiguration();

try {
    (new \OpenAPI\Client\Api\UserApi(config: $config))->deleteUser(
        username: "my_username",
    );
} catch (\OpenAPI\Client\ApiException $e) {
    echo "Exception when calling User#deleteUser: {$e->getMessage()}";
}
