<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$special_event_fields = (new OpenAPIMuseum\Client\Model\SpecialEventFields())
    ->setName("Pirate Coding Workshop")
    ->setLocation("Computer Room")
    ->setEventDescription("Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).")
    ->setPrice(25)
    ->setDates(null);

try {
    $api_caller = new OpenAPIMuseum\Client\Api\EventsApi(config: $config);

    $response = $api_caller->updateSpecialEvent(
        event_id: "dad4bce8-f5cb-4078-a211-995864315e39",
        special_event_fields: $special_event_fields,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#updateSpecialEvent: '
        . print_r($e->getResponseObject());
}
