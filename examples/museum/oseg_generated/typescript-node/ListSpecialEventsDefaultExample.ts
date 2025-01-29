import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.EventsApi();

const startDate = "2023-02-23";
const endDate = "2023-04-18";
const page = 2;
const limit = 15;

apiCaller.listSpecialEvents(
    startDate,
    endDate,
    page,
    limit,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Events#listSpecialEvents:");
  console.log(error.body);
});
