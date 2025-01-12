import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const category: openapi_client.Category = {
    id: 12345,
    name: "Category_Name",
};

const tags_1: openapi_client.Tag = {
    id: 12345,
    name: "tag_1",
};

const tags_2: openapi_client.Tag = {
    id: 98765,
    name: "tag_2",
};

const pet: openapi_client.Pet = {
    name: "My pet name",
    photoUrls: [
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_2.jpg",
    ],
    id: 12345,
    status: openapi_client.Pet.StatusEnum.Available,
    category: category,
    tags: [
        tags_1,
        tags_2,
    ],
};

apiCaller.addPet(
    pet,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#addPet:");
  console.log(error.body);
});
