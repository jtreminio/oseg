import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.StoreApi();

const orderId = undefined;

apiCaller.getOrderById(
    orderId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#getOrderById:");
  console.log(error.body);
});
