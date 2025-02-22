import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const simpleItemSchema = new models.SimpleItemSchema();
simpleItemSchema.code = undefined;
simpleItemSchema.quantity = undefined;

apiCaller.actionTaskTradeMyNameActionTaskTradePost(
  undefined, // name
  simpleItemSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionTaskTradeMyNameActionTaskTradePost:");
  console.log(error.body);
});
