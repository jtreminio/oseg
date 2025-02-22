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
    $response = (new ArtifactsMMO\Client\Api\ItemsApi(config: $config))->getAllItemsItemsGet(
        min_level: null,
        max_level: null,
        name: null,
        type: null,
        craft_skill: null,
        craft_material: null,
        page: 1,
        size: 50,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling Items#getAllItemsItemsGet: {$e->getMessage()}";
}
