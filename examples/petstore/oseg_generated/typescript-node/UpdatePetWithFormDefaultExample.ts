import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const petId = 12345;
const name = "Pet's new name";
const status = "sold";

apiCaller.updatePetWithForm(
    petId,
    name,
    status,
).catch(error => {
  console.log("Exception when calling Pet#updatePetWithForm:");
  console.log(error.body);
});
