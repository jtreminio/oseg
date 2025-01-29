import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const petId = 12345;

apiCaller.getPetById(
    petId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#getPetById:");
  console.log(error.body);
});
