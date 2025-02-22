import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const recyclingSchema = new models.RecyclingSchema();
recyclingSchema.code = undefined;
recyclingSchema.quantity = 1;

apiCaller.actionRecyclingMyNameActionRecyclingPost(
  undefined, // name
  recyclingSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionRecyclingMyNameActionRecyclingPost:");
  console.log(error.body);
});
