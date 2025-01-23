import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

const username = undefined;

apiCaller.getUserByName(
    username,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling User#getUserByName:");
  console.log(error.body);
});
