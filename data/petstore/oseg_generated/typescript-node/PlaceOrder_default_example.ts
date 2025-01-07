import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.StoreApi();

const order: openapi_client.Order = {
    id: 12345,
    petId: 98765,
    quantity: 5,
    shipDate: "2025-01-01T17:32:28Z",
    status: openapi_client.Order.StatusEnum.Approved,
    complete: false,
};

apiCaller.placeOrder(
    order,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Store#placeOrder:");
  console.log(error.body);
});
