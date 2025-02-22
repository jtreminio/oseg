from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    recycling_schema = models.RecyclingSchema(
        code=None,
        quantity=1,
    )

    try:
        response = api.MyCharactersApi(api_client).action_recycling_my_name_action_recycling_post(
            name=None,
            recycling_schema=recycling_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_recycling_my_name_action_recycling_post: %s\n" % e)
