import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.EventsApi();

const specialEvent = new models.SpecialEvent();
specialEvent.name = "Mermaid Treasure Identification and Analysis";
specialEvent.location = "Under the seaaa 🦀 🎶 🌊.";
specialEvent.eventDescription = "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.";
specialEvent.price = 0;
specialEvent.dates = [
    "2023-09-05",
    "2023-09-08",
];
specialEvent.eventId = undefined;

apiCaller.createSpecialEvent(
    specialEvent,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#createSpecialEvent:");
  console.log(error.body);
});
