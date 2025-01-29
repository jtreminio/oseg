import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const tags = [
    "tag_1",
    "tag_2",
];

apiCaller.findPetsByTags(
    tags,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#findPetsByTags:");
  console.log(error.body);
});
