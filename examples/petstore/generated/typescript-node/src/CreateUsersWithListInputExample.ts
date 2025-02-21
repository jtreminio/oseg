import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.UserApi();
apiCaller.setApiKey(api.UserApiApiKeys.api_key, "YOUR_API_KEY");

const user1 = new models.User();
user1.id = 12345;
user1.username = "my_user_1";
user1.firstName = "John";
user1.lastName = "Doe";
user1.email = "john@example.com";
user1.password = "secure_123";
user1.phone = "555-123-1234";
user1.userStatus = 1;

const user2 = new models.User();
user2.id = 67890;
user2.username = "my_user_2";
user2.firstName = "Jane";
user2.lastName = "Doe";
user2.email = "jane@example.com";
user2.password = "secure_456";
user2.phone = "555-123-5678";
user2.userStatus = 2;

const user = [
  user1,
  user2,
];

apiCaller.createUsersWithListInput(
  user,
).catch(error => {
  console.log("Exception when calling User#createUsersWithListInput:");
  console.log(error.body);
});
