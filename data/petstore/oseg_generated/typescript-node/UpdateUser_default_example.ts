import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

const user: openapi_client.User = {
    id: 12345,
    username: "new-username",
    firstName: "Joe",
    lastName: "Broke",
    email: "some-email@example.com",
    password: "so secure omg",
    phone: "555-867-5309",
    userStatus: 1,
};

apiCaller.updateUser(
    username,
    user,
).catch(error => {
  console.log("Exception when calling User#updateUser:");
  console.log(error.body);
});
