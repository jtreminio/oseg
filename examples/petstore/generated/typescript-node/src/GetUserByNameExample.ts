import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.setApiKey(api.UserApiApiKeys.api_key, "YOUR_API_KEY");

apiCaller.getUserByName(
  "my_username", // username
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling User#getUserByName:");
  console.log(error.body);
});
