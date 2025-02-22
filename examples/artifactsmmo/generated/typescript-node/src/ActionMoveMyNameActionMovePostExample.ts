import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.MyCharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const destinationSchema = new models.DestinationSchema();
destinationSchema.x = undefined;
destinationSchema.y = undefined;

apiCaller.actionMoveMyNameActionMovePost(
  undefined, // name
  destinationSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling MyCharacters#actionMoveMyNameActionMovePost:");
  console.log(error.body);
});
