import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const petId = undefined;
apiCaller.updatePetWithForm(
    petId,
).catch(error => {
  console.log("Exception when calling Pet#updatePetWithForm:");
  console.log(error.body);
});
