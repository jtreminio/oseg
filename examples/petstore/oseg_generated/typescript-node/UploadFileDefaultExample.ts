import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

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
