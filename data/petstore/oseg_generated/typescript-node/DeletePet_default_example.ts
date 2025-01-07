import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const petId = undefined;
apiCaller.deletePet(
    petId,
).catch(error => {
  console.log("Exception when calling Pet#deletePet:");
  console.log(error.body);
});
