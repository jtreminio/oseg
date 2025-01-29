import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.UserApi();

apiCaller.logoutUser().catch(error => {
  console.log("Exception when calling User#logoutUser:");
  console.log(error.body);
});
