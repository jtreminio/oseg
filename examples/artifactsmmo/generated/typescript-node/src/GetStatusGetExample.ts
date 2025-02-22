import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.DefaultApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

apiCaller.getStatusGet().then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Default#getStatusGet:");
  console.log(error.body);
});
