<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $api_caller = new OpenAPIMuseum\Client\Api\TicketsApi(config: $config);

    $response = $api_caller->getTicketCode(
        ticket_id: "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Tickets#getTicketCode: '
        . print_r($e->getResponseObject());
}
