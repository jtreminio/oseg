import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const petId = 12345;
const additionalMetadata = undefined;
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
