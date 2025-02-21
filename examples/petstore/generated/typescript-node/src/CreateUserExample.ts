import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();
apiCaller.setApiKey(api.UserApiApiKeys.api_key, "YOUR_API_KEY");

const user = new models.User();
user.id = 12345;
user.username = "my_user";
user.firstName = "John";
user.lastName = "Doe";
user.email = "john@example.com";
user.password = "secure_123";
user.phone = "555-123-1234";
user.userStatus = 1;

apiCaller.createUser(
  user,
).catch(error => {
  console.log("Exception when calling User#createUser:");
  console.log(error.body);
});
