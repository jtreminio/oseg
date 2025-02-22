<?php

namespace OSEG\ArtifactsMMO\Examples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use ArtifactsMMO;

$config = ArtifactsMMO\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$add_character_schema = (new ArtifactsMMO\Client\Model\AddCharacterSchema())
    ->setName(null)
    ->setSkin(null);

try {
    $response = (new ArtifactsMMO\Client\Api\CharactersApi(config: $config))->createCharacterCharactersCreatePost(
        add_character_schema: $add_character_schema,
    );

    print_r($response);
} catch (ArtifactsMMO\Client\ApiException $e) {
    echo "Exception when calling Characters#createCharacterCharactersCreatePost: {$e->getMessage()}";
}
