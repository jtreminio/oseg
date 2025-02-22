<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$ge_order_creationr_schema = (new ArtifactsMMO\Client\Model\GEOrderCreationrSchema())
    ->setCode(null)
    ->setQuantity(null)
    ->setPrice(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionGeCreateSellOrderMyNameActionGrandexchangeSellPost(
        name: null,
        ge_order_creationr_schema: $ge_order_creationr_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionGeCreateSellOrderMyNameActionGrandexchangeSellPost: {$e->getMessage()}";
}
