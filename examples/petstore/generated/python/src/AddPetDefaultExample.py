from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    category = models.Category(
        id=12345,
        name="Category_Name",
    )

    tags_1 = models.Tag(
        id=12345,
        name="tag_1",
    )

    tags_2 = models.Tag(
        id=98765,
        name="tag_2",
    )

    tags = [
        tags_1,
        tags_2,
    ]

    pet = models.Pet(
        name="My pet name",
        photoUrls=[
            "https://example.com/picture_1.jpg",
            "https://example.com/picture_2.jpg",
        ],
        id=12345,
        status="available",
        category=category,
        tags=tags,
    )

    try:
        response = api.PetApi(api_client).add_pet(
            pet=pet,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#add_pet: %s\n" % e)
