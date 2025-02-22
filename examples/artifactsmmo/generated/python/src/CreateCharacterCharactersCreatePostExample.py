from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    add_character_schema = models.AddCharacterSchema(
        name=None,
        skin=None,
    )

    try:
        response = api.CharactersApi(api_client).create_character_characters_create_post(
            add_character_schema=add_character_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Characters#create_character_characters_create_post: %s\n" % e)
