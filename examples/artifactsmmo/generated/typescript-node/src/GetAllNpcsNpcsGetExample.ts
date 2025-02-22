import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.NPCsApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";
// apiCaller.username = "YOUR_USERNAME";
// apiCaller.password = "YOUR_PASSWORD";

apiCaller.getAllNpcsNpcsGet(
  undefined, // type
  1, // page
  50, // size
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling NPCs#getAllNpcsNpcsGet:");
  console.log(error.body);
});
