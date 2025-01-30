import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();

apiCaller.logoutUser().catch(error => {
  console.log("Exception when calling User#logoutUser:");
  console.log(error.body);
});
