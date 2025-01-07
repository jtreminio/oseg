import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.UserApi();

const user_1: openapi_client.User = {
    id: 12345,
    username: "my_user",
    firstName: "John",
    lastName: "Doe",
    email: "john@example.com",
    password: "secure_123",
    phone: "555-123-1234",
    userStatus: 1,
};

const user_2: openapi_client.User = {
    id: 12345,
    username: "my_user",
    firstName: "John",
    lastName: "Doe",
    email: "john@example.com",
    password: "secure_123",
    phone: "555-123-1234",
    userStatus: 1,
};

const user = [
    user_1,
    user_2,
];

apiCaller.createUsersWithListInput(
    user,
).catch(error => {
  console.log("Exception when calling User#createUsersWithListInput:");
  console.log(error.body);
});
