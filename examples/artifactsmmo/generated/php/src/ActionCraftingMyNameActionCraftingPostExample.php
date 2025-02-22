<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$crafting_schema = (new ArtifactsMMO\Client\Model\CraftingSchema())
    ->setCode(null)
    ->setQuantity(1);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionCraftingMyNameActionCraftingPost(
        name: null,
        crafting_schema: $crafting_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionCraftingMyNameActionCraftingPost: {$e->getMessage()}";
}
