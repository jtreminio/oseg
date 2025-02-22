from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    crafting_schema = models.CraftingSchema(
        code=None,
        quantity=1,
    )

    try:
        response = api.MyCharactersApi(api_client).action_crafting_my_name_action_crafting_post(
            name=None,
            crafting_schema=crafting_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_crafting_my_name_action_crafting_post: %s\n" % e)
