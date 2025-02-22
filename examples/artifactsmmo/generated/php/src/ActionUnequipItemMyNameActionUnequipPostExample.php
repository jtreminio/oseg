<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$unequip_schema = (new ArtifactsMMO\Client\Model\UnequipSchema())
    ->setSlot(null)
    ->setQuantity(1);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionUnequipItemMyNameActionUnequipPost(
        name: null,
        unequip_schema: $unequip_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionUnequipItemMyNameActionUnequipPost: {$e->getMessage()}";
}
