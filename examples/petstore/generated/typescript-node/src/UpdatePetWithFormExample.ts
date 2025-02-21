import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

apiCaller.updatePetWithForm(
  12345, // petId
  "Pet's new name", // name
  "sold", // status
).catch(error => {
  console.log("Exception when calling Pet#updatePetWithForm:");
  console.log(error.body);
});
