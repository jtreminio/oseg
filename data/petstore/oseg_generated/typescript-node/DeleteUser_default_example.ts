import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

const username = undefined;
apiCaller.deleteUser(
    username,
).catch(error => {
  console.log("Exception when calling User#deleteUser:");
  console.log(error.body);
});
