<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$destination_schema = (new ArtifactsMMO\Client\Model\DestinationSchema())
    ->setX(null)
    ->setY(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionMoveMyNameActionMovePost(
        name: null,
        destination_schema: $destination_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionMoveMyNameActionMovePost: {$e->getMessage()}";
}
