<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPIMuseum\Client\Api\OperationsApi(config: $config);

    $response = $api_caller->getMuseumHours(
        start_date: "2023-02-23",
        page: 2,
        limit: 15,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Operations#getMuseumHours: '
        . print_r($e->getResponseObject());
}
