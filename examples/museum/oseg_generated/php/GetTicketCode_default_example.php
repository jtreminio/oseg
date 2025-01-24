<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

try {
    $response = (new OpenAPIMuseum\Client\Api\TicketsApi($config))->getTicketCode(
        ticket_id: "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
    );

    copy($response->getRealPath(), __DIR__ . '/file_response.zip');
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Tickets#getTicketCode: '
        . print_r($e->getResponseObject());
}
