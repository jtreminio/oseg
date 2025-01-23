import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const tags = undefined;

apiCaller.findPetsByTags(
    tags,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#findPetsByTags:");
  console.log(error.body);
});
