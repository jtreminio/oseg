<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->getAllCharactersLogsMyLogsGet(
        page: 1,
        size: 50,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#getAllCharactersLogsMyLogsGet: {$e->getMessage()}";
}
