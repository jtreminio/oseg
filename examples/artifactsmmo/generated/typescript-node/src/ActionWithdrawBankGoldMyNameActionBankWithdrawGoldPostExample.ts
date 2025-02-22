import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const depositWithdrawGoldSchema = new models.DepositWithdrawGoldSchema();
depositWithdrawGoldSchema.quantity = undefined;

apiCaller.actionWithdrawBankGoldMyNameActionBankWithdrawGoldPost(
  undefined, // name
  depositWithdrawGoldSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionWithdrawBankGoldMyNameActionBankWithdrawGoldPost:");
  console.log(error.body);
});
