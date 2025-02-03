<?php

namespace OSEG\PetStore\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

$user = (new OpenAPI\Client\Model\User())
    ->setId(12345)
    ->setUsername("new-username")
    ->setFirstName("Joe")
    ->setLastName("Broke")
    ->setEmail("some-email@example.com")
    ->setPassword("so secure omg")
    ->setPhone("555-867-5309")
    ->setUserStatus(1);

try {
    (new OpenAPI\Client\Api\UserApi(config: $config))->updateUser(
        username: "my-username",
        user: $user,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling User#updateUser: {$e->getMessage()}";
}
