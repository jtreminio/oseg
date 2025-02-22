<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$change_password = (new ArtifactsMMO\Client\Model\ChangePassword())
    ->setCurrentPassword(null)
    ->setNewPassword(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyAccountApi(config: $config))->changePasswordMyChangePasswordPost(
        change_password: $change_password,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyAccount#changePasswordMyChangePasswordPost: {$e->getMessage()}";
}
