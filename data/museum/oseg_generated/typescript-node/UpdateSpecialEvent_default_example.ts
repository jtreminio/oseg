import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const special_event_fields: openapimuseum_client.SpecialEventFields = {
    name: "Pirate Coding Workshop",
    location: "Computer Room",
    eventDescription: "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
    price: 25,
    dates: undefined,
};

apiCaller.updateSpecialEvent(
    eventId,
    specialEventFields,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#updateSpecialEvent:");
  console.log(error.body);
});
