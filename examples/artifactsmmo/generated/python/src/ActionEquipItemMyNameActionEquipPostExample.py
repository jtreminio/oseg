from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    equip_schema = models.EquipSchema(
        code=None,
        slot=None,
        quantity=1,
    )

    try:
        response = api.MyCharactersApi(api_client).action_equip_item_my_name_action_equip_post(
            name=None,
            equip_schema=equip_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_equip_item_my_name_action_equip_post: %s\n" % e)
