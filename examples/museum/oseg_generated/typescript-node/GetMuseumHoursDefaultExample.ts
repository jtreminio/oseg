import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.OperationsApi();

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
