from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    unequip_schema = models.UnequipSchema(
        slot=None,
        quantity=1,
    )

    try:
        response = api.MyCharactersApi(api_client).action_unequip_item_my_name_action_unequip_post(
            name=None,
            unequip_schema=unequip_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_unequip_item_my_name_action_unequip_post: %s\n" % e)
