import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const status = [
    "available",
    "pending",
] as Array<"available" | "pending">;

apiCaller.findPetsByStatus(
    status,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#findPetsByStatus:");
  console.log(error.body);
});
