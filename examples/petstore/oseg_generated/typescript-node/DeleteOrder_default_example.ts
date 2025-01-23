import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.StoreApi();

const orderId = undefined;

apiCaller.deleteOrder(
    orderId,
).catch(error => {
  console.log("Exception when calling Store#deleteOrder:");
  console.log(error.body);
});
