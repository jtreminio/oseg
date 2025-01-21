import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.EventsApi();

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
