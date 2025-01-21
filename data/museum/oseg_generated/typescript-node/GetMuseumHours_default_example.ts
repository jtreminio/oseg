import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.OperationsApi();

const startDate = "2023-02-23";
const page = 2;
const limit = 15;

apiCaller.getMuseumHours(
    startDate,
    page,
    limit,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Operations#getMuseumHours:");
  console.log(error.body);
});
