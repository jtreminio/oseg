import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyAccountApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

apiCaller.getBankItemsMyBankItemsGet(
  undefined, // itemCode
  1, // page
  50, // size
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyAccount#getBankItemsMyBankItemsGet:");
  console.log(error.body);
});
