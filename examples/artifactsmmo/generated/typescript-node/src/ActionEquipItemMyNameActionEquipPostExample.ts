import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const equipSchema = new models.EquipSchema();
equipSchema.code = undefined;
equipSchema.slot = undefined;
equipSchema.quantity = 1;

apiCaller.actionEquipItemMyNameActionEquipPost(
  undefined, // name
  equipSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionEquipItemMyNameActionEquipPost:");
  console.log(error.body);
});
