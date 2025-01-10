import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

const eventId = "dad4bce8-f5cb-4078-a211-995864315e39";
apiCaller.getSpecialEvent(
    eventId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#getSpecialEvent:");
  console.log(error.body);
});
