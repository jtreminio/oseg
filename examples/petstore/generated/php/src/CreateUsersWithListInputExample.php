<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setApiKey("api_key", "YOUR_API_KEY");

$user_1 = (new OpenAPI\Client\Model\User())
    ->setId(12345)
    ->setUsername("my_user_1")
    ->setFirstName("John")
    ->setLastName("Doe")
    ->setEmail("john@example.com")
    ->setPassword("secure_123")
    ->setPhone("555-123-1234")
    ->setUserStatus(1);

$user_2 = (new OpenAPI\Client\Model\User())
    ->setId(67890)
    ->setUsername("my_user_2")
    ->setFirstName("Jane")
    ->setLastName("Doe")
    ->setEmail("jane@example.com")
    ->setPassword("secure_456")
    ->setPhone("555-123-5678")
    ->setUserStatus(2);

$user = [
    $user_1,
    $user_2,
];

try {
    (new OpenAPI\Client\Api\UserApi(config: $config))->createUsersWithListInput(
        user: $user,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling User#createUsersWithListInput: {$e->getMessage()}";
}
