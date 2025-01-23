import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const status = undefined;

apiCaller.findPetsByStatus(
    status,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#findPetsByStatus:");
  console.log(error.body);
});
