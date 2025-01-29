import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.UserApi();

const username = "my_username";
const password = "my_secret_password";

apiCaller.loginUser(
    username,
    password,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling User#loginUser:");
  console.log(error.body);
});
