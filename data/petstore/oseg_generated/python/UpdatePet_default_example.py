from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    category = models.Category()
    category.id = 12345
    category.name = "Category_Name"

    tags_1 = models.Tag()
    tags_1.id = 12345
    tags_1.name = "tag_1"

    tags_2 = models.Tag()
    tags_2.id = 98765
    tags_2.name = "tag_2"

    pet = models.Pet()
    pet.name = "My pet name"
    pet.photoUrls = [
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_1.jpg",
    ]
    pet.id = 12345
    pet.status = "available"
    pet.category = category
    pet.tags = [
        tags_1,
        tags_2,
    ]

    try:
        api_caller = api.PetApi(api_client)

        response = api_caller.update_pet(
            pet=pet,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#update_pet: %s\n" % e)
