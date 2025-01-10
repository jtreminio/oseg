<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPIMuseum\Client\Api\EventsApi(config: $config);

    $response = $api_caller->listSpecialEvents(
        start_date: "2023-02-23",
        end_date: "2023-04-18",
        page: 2,
        limit: 15,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#listSpecialEvents: '
        . print_r($e->getResponseObject());
}
