import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.StoreApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.setApiKey(api.StoreApiApiKeys.api_key, "YOUR_API_KEY");

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
