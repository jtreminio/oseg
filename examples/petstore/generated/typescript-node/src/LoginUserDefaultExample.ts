import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();

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
