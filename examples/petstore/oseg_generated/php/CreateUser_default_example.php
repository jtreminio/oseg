<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

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
    $api_caller = new OpenAPI\Client\Api\UserApi(config: $config);

    $api_caller->createUser(
        user: $user,
    );
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling User#createUser: '
        . print_r($e->getResponseObject());
}
