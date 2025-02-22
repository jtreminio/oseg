from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.MyCharactersApi(api_client).action_fight_my_name_action_fight_post(
            name=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_fight_my_name_action_fight_post: %s\n" % e)
