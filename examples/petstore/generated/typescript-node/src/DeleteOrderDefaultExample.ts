import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.StoreApi();

const orderId = "12345";

apiCaller.deleteOrder(
    orderId,
).catch(error => {
  console.log("Exception when calling Store#deleteOrder:");
  console.log(error.body);
});
