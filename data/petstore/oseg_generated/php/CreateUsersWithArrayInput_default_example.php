<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

$user_1 = (new OpenAPI\Client\Model\User())
    ->setId(12345)
    ->setUsername("my_user")
    ->setFirstName("John")
    ->setLastName("Doe")
    ->setEmail("john@example.com")
    ->setPassword("secure_123")
    ->setPhone("555-123-1234")
    ->setUserStatus(1);

$user_2 = (new OpenAPI\Client\Model\User())
    ->setId(12345)
    ->setUsername("my_user")
    ->setFirstName("John")
    ->setLastName("Doe")
    ->setEmail("john@example.com")
    ->setPassword("secure_123")
    ->setPhone("555-123-1234")
    ->setUserStatus(1);

$user = [
    $user_1,
    $user_2,
];

try {
    $api_caller = new OpenAPI\Client\Api\UserApi(config: $config);

    $api_caller->createUsersWithArrayInput(
        user: $user,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#createUsersWithArrayInput: '
        . print_r($e->getResponseObject());
}
