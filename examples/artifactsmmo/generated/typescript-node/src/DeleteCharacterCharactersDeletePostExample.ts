import * as fs from 'fs';
import api from "artifacts_mmo_client"
import models from "artifacts_mmo_client"

const apiCaller = new api.CharactersApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const deleteCharacterSchema = new models.DeleteCharacterSchema();
deleteCharacterSchema.name = undefined;

apiCaller.deleteCharacterCharactersDeletePost(
  deleteCharacterSchema,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Characters#deleteCharacterCharactersDeletePost:");
  console.log(error.body);
});
