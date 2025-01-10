import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const special_event: openapimuseum_client.SpecialEvent = {
    name: "Mermaid Treasure Identification and Analysis",
    location: "Under the seaaa 🦀 🎶 🌊.",
    eventDescription: "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
    price: 0,
    eventId: undefined,
};

apiCaller.createSpecialEvent(
    specialEvent,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#createSpecialEvent:");
  console.log(error.body);
});
