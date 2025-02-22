from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    delete_character_schema = models.DeleteCharacterSchema(
        name=None,
    )

    try:
        response = api.CharactersApi(api_client).delete_character_characters_delete_post(
            delete_character_schema=delete_character_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Characters#delete_character_characters_delete_post: %s\n" % e)
