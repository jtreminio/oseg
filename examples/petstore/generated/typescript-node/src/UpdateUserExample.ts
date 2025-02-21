import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();
apiCaller.setApiKey(api.UserApiApiKeys.api_key, "YOUR_API_KEY");

const user = new models.User();
user.id = 12345;
user.username = "new-username";
user.firstName = "Joe";
user.lastName = "Broke";
user.email = "some-email@example.com";
user.password = "so secure omg";
user.phone = "555-867-5309";
user.userStatus = 1;

apiCaller.updateUser(
  "my-username", // username
  user,
).catch(error => {
  console.log("Exception when calling User#updateUser:");
  console.log(error.body);
});
