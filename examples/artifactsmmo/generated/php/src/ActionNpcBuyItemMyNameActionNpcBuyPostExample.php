<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$npc_merchant_buy_schema = (new ArtifactsMMO\Client\Model\NpcMerchantBuySchema())
    ->setCode(null)
    ->setQuantity(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionNpcBuyItemMyNameActionNpcBuyPost(
        name: null,
        npc_merchant_buy_schema: $npc_merchant_buy_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionNpcBuyItemMyNameActionNpcBuyPost: {$e->getMessage()}";
}
