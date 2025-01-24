<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPIMuseum\Client\Configuration::getDefaultConfiguration();

$special_event = (new OpenAPIMuseum\Client\Model\SpecialEvent())
    ->setName("Mermaid Treasure Identification and Analysis")
    ->setLocation("Under the seaaa 🦀 🎶 🌊.")
    ->setEventDescription("Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.")
    ->setPrice(0)
    ->setDates([
        new \DateTime("2023-09-05"),
        new \DateTime("2023-09-08"),
    ])
    ->setEventId(null);

try {
    $response = (new OpenAPIMuseum\Client\Api\EventsApi($config))->createSpecialEvent(
        special_event: $special_event,
    );

    print_r($response);
} catch (OpenAPIMuseum\Client\ApiException $e) {
    echo 'Exception when calling Events#createSpecialEvent: '
        . print_r($e->getResponseObject());
}
