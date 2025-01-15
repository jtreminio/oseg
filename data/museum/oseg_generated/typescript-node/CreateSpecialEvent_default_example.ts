import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const special_event: openapimuseum_client.SpecialEvent = {
    name: "Pirate Coding Workshop",
    location: "Computer Room",
    eventDescription: "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
    price: 25,
    dates: [
        "2023-09-05",
        "2023-09-08",
    ],
    eventId: "3be6453c-03eb-4357-ae5a-984a0e574a54",
};

apiCaller.createSpecialEvent(
    specialEvent,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#createSpecialEvent:");
  console.log(error.body);
});
