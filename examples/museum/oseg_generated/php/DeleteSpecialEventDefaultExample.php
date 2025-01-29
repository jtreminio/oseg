<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    (new OpenAPIMuseum\Client\Api\EventsApi(config: $config))->deleteSpecialEvent(
        event_id: "dad4bce8-f5cb-4078-a211-995864315e39",
    );
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#deleteSpecialEvent: '
        . print_r($e->getResponseObject());
}
