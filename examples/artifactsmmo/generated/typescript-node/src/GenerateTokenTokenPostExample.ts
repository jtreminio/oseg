import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.TokenApi();
apiCaller.username = "YOUR_USERNAME";
apiCaller.password = "YOUR_PASSWORD";

apiCaller.generateTokenTokenPost().then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Token#generateTokenTokenPost:");
  console.log(error.body);
});
