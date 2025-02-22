<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$ge_cancel_order_schema = (new ArtifactsMMO\Client\Model\GECancelOrderSchema())
    ->setId(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionGeCancelSellOrderMyNameActionGrandexchangeCancelPost(
        name: null,
        ge_cancel_order_schema: $ge_cancel_order_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionGeCancelSellOrderMyNameActionGrandexchangeCancelPost: {$e->getMessage()}";
}
