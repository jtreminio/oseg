from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    destination_schema = models.DestinationSchema(
        x=None,
        y=None,
    )

    try:
        response = api.MyCharactersApi(api_client).action_move_my_name_action_move_post(
            name=None,
            destination_schema=destination_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_move_my_name_action_move_post: %s\n" % e)
