import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const unequipSchema = new models.UnequipSchema();
unequipSchema.slot = undefined;
unequipSchema.quantity = 1;

apiCaller.actionUnequipItemMyNameActionUnequipPost(
  undefined, // name
  unequipSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionUnequipItemMyNameActionUnequipPost:");
  console.log(error.body);
});
