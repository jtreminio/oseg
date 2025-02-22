<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$deposit_withdraw_gold_schema = (new ArtifactsMMO\Client\Model\DepositWithdrawGoldSchema())
    ->setQuantity(null);

try {
    $response = (new ArtifactsMMO\Client\Api\MyCharactersApi(config: $config))->actionDepositBankGoldMyNameActionBankDepositGoldPost(
        name: null,
        deposit_withdraw_gold_schema: $deposit_withdraw_gold_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling MyCharacters#actionDepositBankGoldMyNameActionBankDepositGoldPost: {$e->getMessage()}";
}
