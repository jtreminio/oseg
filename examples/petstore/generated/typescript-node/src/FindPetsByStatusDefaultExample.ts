import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

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
