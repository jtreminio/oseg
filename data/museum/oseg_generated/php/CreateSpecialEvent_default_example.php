<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$special_event = (new OpenAPIMuseum\Client\Model\SpecialEvent())
    ->setName("Pirate Coding Workshop")
    ->setLocation("Computer Room")
    ->setEventDescription("Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).")
    ->setPrice(25)
    ->setDates([
        "2023-09-05",
        "2023-09-08",
    ])
    ->setEventId("3be6453c-03eb-4357-ae5a-984a0e574a54");

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
