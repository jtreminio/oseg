import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.StoreApi();

const orderId = 3;

apiCaller.getOrderById(
    orderId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#getOrderById:");
  console.log(error.body);
});
