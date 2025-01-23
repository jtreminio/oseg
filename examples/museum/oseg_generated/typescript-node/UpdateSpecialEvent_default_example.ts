import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const specialEventFields: openapimuseum_client.SpecialEventFields = {
    name: undefined,
    location: "On the beach.",
    eventDescription: undefined,
    price: 15,
    dates: undefined,
};

const eventId = "dad4bce8-f5cb-4078-a211-995864315e39";

apiCaller.updateSpecialEvent(
    eventId,
    specialEventFields,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#updateSpecialEvent:");
  console.log(error.body);
});
