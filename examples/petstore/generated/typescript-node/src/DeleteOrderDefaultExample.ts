import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.StoreApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
apiCaller.setApiKey(api.StoreApiApiKeys.api_key, "YOUR_API_KEY");

const orderId = "12345";

apiCaller.deleteOrder(
    orderId,
).catch(error => {
  console.log("Exception when calling Store#deleteOrder:");
  console.log(error.body);
});
