<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$delete_character_schema = (new ArtifactsMMO\Client\Model\DeleteCharacterSchema())
    ->setName(null);

try {
    $response = (new ArtifactsMMO\Client\Api\CharactersApi(config: $config))->deleteCharacterCharactersDeletePost(
        delete_character_schema: $delete_character_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling Characters#deleteCharacterCharactersDeletePost: {$e->getMessage()}";
}
