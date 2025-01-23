import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.StoreApi();

apiCaller.getInventory().then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#getInventory:");
  console.log(error.body);
});
