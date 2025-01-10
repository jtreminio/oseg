import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const special_event: openapimuseum_client.SpecialEvent = {
};

apiCaller.createSpecialEvent(
    specialEvent,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#createSpecialEvent:");
  console.log(error.body);
});
