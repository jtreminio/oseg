import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.GrandExchangeApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

apiCaller.getGeSellOrdersGrandexchangeOrdersGet(
  undefined, // code
  undefined, // seller
  1, // page
  50, // size
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling GrandExchange#getGeSellOrdersGrandexchangeOrdersGet:");
  console.log(error.body);
});
