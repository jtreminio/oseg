import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

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
