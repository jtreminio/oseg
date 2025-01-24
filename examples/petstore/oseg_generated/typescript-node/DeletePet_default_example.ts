import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const petId = 12345;
const apiKey = "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a";

apiCaller.deletePet(
    petId,
    apiKey,
).catch(error => {
  console.log("Exception when calling Pet#deletePet:");
  console.log(error.body);
});
