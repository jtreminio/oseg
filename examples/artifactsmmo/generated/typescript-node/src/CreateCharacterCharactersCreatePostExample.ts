import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.CharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const addCharacterSchema = new models.AddCharacterSchema();
addCharacterSchema.name = undefined;
addCharacterSchema.skin = undefined;

apiCaller.createCharacterCharactersCreatePost(
  addCharacterSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Characters#createCharacterCharactersCreatePost:");
  console.log(error.body);
});
