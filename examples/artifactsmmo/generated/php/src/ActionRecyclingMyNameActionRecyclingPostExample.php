<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$recycling_schema = (new ArtifactsMMO\Client\Model\RecyclingSchema())
    ->setCode(null)
    ->setQuantity(1);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionRecyclingMyNameActionRecyclingPost(
        name: null,
        recycling_schema: $recycling_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionRecyclingMyNameActionRecyclingPost: {$e->getMessage()}";
}
