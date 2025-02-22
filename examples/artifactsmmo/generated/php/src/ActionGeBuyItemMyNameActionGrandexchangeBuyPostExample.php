<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$ge_buy_order_schema = (new ArtifactsMMO\Client\Model\GEBuyOrderSchema())
    ->setId(null)
    ->setQuantity(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionGeBuyItemMyNameActionGrandexchangeBuyPost(
        name: null,
        ge_buy_order_schema: $ge_buy_order_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionGeBuyItemMyNameActionGrandexchangeBuyPost: {$e->getMessage()}";
}
