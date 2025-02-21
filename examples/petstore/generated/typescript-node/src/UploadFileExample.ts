import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

apiCaller.uploadFile(
  12345, // petId
  "Additional data to pass to server", // additionalMetadata
  fs.createReadStream("/path/to/file"), // file
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#uploadFile:");
  console.log(error.body);
});
