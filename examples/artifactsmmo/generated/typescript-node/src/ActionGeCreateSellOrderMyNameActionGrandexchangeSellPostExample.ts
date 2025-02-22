import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const gEOrderCreationrSchema = new models.GEOrderCreationrSchema();
gEOrderCreationrSchema.code = undefined;
gEOrderCreationrSchema.quantity = undefined;
gEOrderCreationrSchema.price = undefined;

apiCaller.actionGeCreateSellOrderMyNameActionGrandexchangeSellPost(
  undefined, // name
  gEOrderCreationrSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionGeCreateSellOrderMyNameActionGrandexchangeSellPost:");
  console.log(error.body);
});
