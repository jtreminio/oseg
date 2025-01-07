import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const petId = undefined;
apiCaller.getPetById(
    petId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#getPetById:");
  console.log(error.body);
});
