<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");
// $config->setUsername("YOUR_USERNAME");
// $config->setPassword("YOUR_PASSWORD");

try {
    $response = (new ArtifactsMMO\Client\Api\MonstersApi(config: $config))->getMonsterMonstersCodeGet(
        code: null,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling Monsters#getMonsterMonstersCodeGet: {$e->getMessage()}";
}
