import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.StoreApi();

const order = new models.Order();
order.id = 12345;
order.petId = 98765;
order.quantity = 5;
order.shipDate = new Date("2025-01-01T17:32:28Z");
order.status = models.Order.StatusEnum.Approved;
order.complete = false;

apiCaller.placeOrder(
    order,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#placeOrder:");
  console.log(error.body);
});
