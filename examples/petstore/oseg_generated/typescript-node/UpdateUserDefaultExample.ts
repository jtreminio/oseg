import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.UserApi();

const user = new models.User();
user.id = 12345;
user.username = "new-username";
user.firstName = "Joe";
user.lastName = "Broke";
user.email = "some-email@example.com";
user.password = "so secure omg";
user.phone = "555-867-5309";
user.userStatus = 1;

const username = "my-username";

apiCaller.updateUser(
    username,
    user,
).catch(error => {
  console.log("Exception when calling User#updateUser:");
  console.log(error.body);
});
