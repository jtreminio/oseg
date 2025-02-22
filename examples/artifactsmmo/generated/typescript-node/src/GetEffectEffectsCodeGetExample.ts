import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.EffectsApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

apiCaller.getEffectEffectsCodeGet(
  undefined, // code
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Effects#getEffectEffectsCodeGet:");
  console.log(error.body);
});
