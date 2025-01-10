<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$special_event = (new OpenAPIMuseum\Client\Model\SpecialEvent());

try {
    $api_caller = new OpenAPIMuseum\Client\Api\EventsApi(config: $config);

    $response = $api_caller->createSpecialEvent(
        special_event: $special_event,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#createSpecialEvent: '
        . print_r($e->getResponseObject());
}
