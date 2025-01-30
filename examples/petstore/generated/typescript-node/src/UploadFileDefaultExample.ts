import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();

const petId = 12345;
const additionalMetadata = "Additional data to pass to server";
const file = fs.createReadStream("/path/to/file");

apiCaller.uploadFile(
    petId,
    additionalMetadata,
    file,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#uploadFile:");
  console.log(error.body);
});
