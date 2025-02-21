import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();
apiCaller.setApiKey(api.UserApiApiKeys.api_key, "YOUR_API_KEY");

apiCaller.deleteUser(
  "my_username", // username
).catch(error => {
  console.log("Exception when calling User#deleteUser:");
  console.log(error.body);
});
