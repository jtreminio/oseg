import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.StoreApi();

apiCaller.getInventory().then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#getInventory:");
  console.log(error.body);
});
