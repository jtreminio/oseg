import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.StoreApi();

const orderId = 3;

apiCaller.getOrderById(
    orderId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#getOrderById:");
  console.log(error.body);
});
