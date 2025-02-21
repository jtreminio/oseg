import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

apiCaller.findPetsByTags(
  [
    "tag_1",
    "tag_2",
  ], // tags
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#findPetsByTags:");
  console.log(error.body);
});
