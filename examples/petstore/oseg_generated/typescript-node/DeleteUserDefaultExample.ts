import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.UserApi();

const username = "my_username";

apiCaller.deleteUser(
    username,
).catch(error => {
  console.log("Exception when calling User#deleteUser:");
  console.log(error.body);
});
