import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const petId = 12345;
const apiKey = "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a";

apiCaller.deletePet(
    petId,
    apiKey,
).catch(error => {
  console.log("Exception when calling Pet#deletePet:");
  console.log(error.body);
});
