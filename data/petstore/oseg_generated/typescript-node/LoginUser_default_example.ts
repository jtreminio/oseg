import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

const username = undefined;
const password = undefined;

apiCaller.loginUser(
    username,
    password,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling User#loginUser:");
  console.log(error.body);
});
