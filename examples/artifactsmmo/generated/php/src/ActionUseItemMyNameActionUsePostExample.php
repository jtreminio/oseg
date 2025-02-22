<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$simple_item_schema = (new ArtifactsMMO\Client\Model\SimpleItemSchema())
    ->setCode(null)
    ->setQuantity(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionUseItemMyNameActionUsePost(
        name: null,
        simple_item_schema: $simple_item_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionUseItemMyNameActionUsePost: {$e->getMessage()}";
}
