import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.StoreApi();

const orderId = "12345";

apiCaller.deleteOrder(
    orderId,
).catch(error => {
  console.log("Exception when calling Store#deleteOrder:");
  console.log(error.body);
});
