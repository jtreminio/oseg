import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const npcMerchantBuySchema = new models.NpcMerchantBuySchema();
npcMerchantBuySchema.code = undefined;
npcMerchantBuySchema.quantity = undefined;

apiCaller.actionNpcBuyItemMyNameActionNpcBuyPost(
  undefined, // name
  npcMerchantBuySchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionNpcBuyItemMyNameActionNpcBuyPost:");
  console.log(error.body);
});
