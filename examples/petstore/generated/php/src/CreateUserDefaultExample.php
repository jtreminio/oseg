<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setApiKey("api_key", "YOUR_API_KEY");

$user = (new OpenAPI\Client\Model\User())
    ->setId(12345)
    ->setUsername("my_user")
    ->setFirstName("John")
    ->setLastName("Doe")
    ->setEmail("john@example.com")
    ->setPassword("secure_123")
    ->setPhone("555-123-1234")
    ->setUserStatus(1);

try {
    (new OpenAPI\Client\Api\UserApi(config: $config))->createUser(
        user: $user,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling User#createUser: {$e->getMessage()}";
}
