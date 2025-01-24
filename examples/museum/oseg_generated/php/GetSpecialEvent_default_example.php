<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPIMuseum\Client\Api\EventsApi($config))->getSpecialEvent(
        event_id: "dad4bce8-f5cb-4078-a211-995864315e39",
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#getSpecialEvent: '
        . print_r($e->getResponseObject());
}
