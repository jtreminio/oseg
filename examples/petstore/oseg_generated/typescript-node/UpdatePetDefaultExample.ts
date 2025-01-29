import * as fs from 'fs';
import * as apis from "openapi_client/api/apis"
import * as models from "openapi_client/model/models"

const apiCaller = new apis.PetApi();

const category = new models.Category();
category.id = 12345;
category.name = "Category_Name";

const tags1 = new models.Tag();
tags1.id = 12345;
tags1.name = "tag_1";

const tags2 = new models.Tag();
tags2.id = 98765;
tags2.name = "tag_2";

const tags = [
    tags1,
    tags2,
];

const pet = new models.Pet();
pet.name = "My pet name";
pet.photoUrls = [
    "https://example.com/picture_1.jpg",
    "https://example.com/picture_2.jpg",
];
pet.id = 12345;
pet.status = models.Pet.StatusEnum.Available;
pet.category = category;
pet.tags = tags;

apiCaller.updatePet(
    pet,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#updatePet:");
  console.log(error.body);
});
