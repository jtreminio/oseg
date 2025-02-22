<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");
// $config->setUsername("YOUR_USERNAME");
// $config->setPassword("YOUR_PASSWORD");

$add_account_schema = (new ArtifactsMMO\Client\Model\AddAccountSchema())
    ->setUsername(null)
    ->setPassword(null)
    ->setEmail(null);

try {
    $response = (new ArtifactsMMO\Client\Api\AccountsApi(config: $config))->createAccountAccountsCreatePost(
        add_account_schema: $add_account_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling Accounts#createAccountAccountsCreatePost: {$e->getMessage()}";
}
