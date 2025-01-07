import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

apiCaller.logoutUser(
).catch(error => {
  console.log("Exception when calling User#logoutUser:");
  console.log(error.body);
});
