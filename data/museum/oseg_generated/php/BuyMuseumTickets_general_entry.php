<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$buy_museum_tickets = (new OpenAPIMuseum\Client\Model\BuyMuseumTickets());

try {
    $api_caller = new OpenAPIMuseum\Client\Api\TicketsApi(config: $config);

    $response = $api_caller->buyMuseumTickets(
        buy_museum_tickets: $buy_museum_tickets,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Tickets#buyMuseumTickets: '
        . print_r($e->getResponseObject());
}
