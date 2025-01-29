import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.EventsApi();

const eventId = "dad4bce8-f5cb-4078-a211-995864315e39";

apiCaller.getSpecialEvent(
    eventId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#getSpecialEvent:");
  console.log(error.body);
});
