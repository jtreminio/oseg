<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$equip_schema = (new ArtifactsMMO\Client\Model\EquipSchema())
    ->setCode(null)
    ->setSlot(null)
    ->setQuantity(1);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionEquipItemMyNameActionEquipPost(
        name: null,
        equip_schema: $equip_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionEquipItemMyNameActionEquipPost: {$e->getMessage()}";
}
