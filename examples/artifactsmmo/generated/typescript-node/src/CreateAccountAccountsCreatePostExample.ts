import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.AccountsApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

const addAccountSchema = new models.AddAccountSchema();
addAccountSchema.username = undefined;
addAccountSchema.password = undefined;
addAccountSchema.email = undefined;

apiCaller.createAccountAccountsCreatePost(
  addAccountSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Accounts#createAccountAccountsCreatePost:");
  console.log(error.body);
});
