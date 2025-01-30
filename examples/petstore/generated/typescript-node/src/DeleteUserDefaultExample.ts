import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();

const username = "my_username";

apiCaller.deleteUser(
    username,
).catch(error => {
  console.log("Exception when calling User#deleteUser:");
  console.log(error.body);
});
