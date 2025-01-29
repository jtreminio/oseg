import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.UserApi();

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
