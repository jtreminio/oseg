import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.AccountsApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

apiCaller.getAccountAccountsAccountGet(
  undefined, // account
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Accounts#getAccountAccountsAccountGet:");
  console.log(error.body);
});
