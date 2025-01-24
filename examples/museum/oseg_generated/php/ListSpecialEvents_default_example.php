<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPIMuseum\Client\Api\EventsApi($config))->listSpecialEvents(
        start_date: new \DateTime("2023-02-23"),
        end_date: new \DateTime("2023-04-18"),
        page: 2,
        limit: 15,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#listSpecialEvents: '
        . print_r($e->getResponseObject());
}
