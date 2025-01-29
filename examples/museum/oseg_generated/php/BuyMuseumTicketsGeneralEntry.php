<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$buy_museum_tickets = (new OpenAPIMuseum\Client\Model\BuyMuseumTickets())
    ->setTicketType(OpenAPIMuseum\Client\Model\BuyMuseumTickets::TICKETTYPE_GENERAL)
    ->setTicketDate(new \DateTime("2023-09-07"))
    ->setEmail("todd@example.com")
    ->setTicketId(null)
    ->setEventId(null);

try {
    $response = (new OpenAPIMuseum\Client\Api\TicketsApi(config: $config))->buyMuseumTickets(
        buy_museum_tickets: $buy_museum_tickets,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Tickets#buyMuseumTickets: '
        . print_r($e->getResponseObject());
}
