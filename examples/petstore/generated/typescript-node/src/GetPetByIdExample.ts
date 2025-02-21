import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.setApiKey(api.PetApiApiKeys.api_key, "YOUR_API_KEY");

apiCaller.getPetById(
  12345, // petId
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#getPetById:");
  console.log(error.body);
});
