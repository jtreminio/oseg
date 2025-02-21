import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

apiCaller.deletePet(
  12345, // petId
  "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a", // apiKey
).catch(error => {
  console.log("Exception when calling Pet#deletePet:");
  console.log(error.body);
});
