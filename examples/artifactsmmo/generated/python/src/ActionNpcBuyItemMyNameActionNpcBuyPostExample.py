from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    npc_merchant_buy_schema = models.NpcMerchantBuySchema(
        code=None,
        quantity=None,
    )

    try:
        response = api.MyCharactersApi(api_client).action_npc_buy_item_my_name_action_npc_buy_post(
            name=None,
            npc_merchant_buy_schema=npc_merchant_buy_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_npc_buy_item_my_name_action_npc_buy_post: %s\n" % e)
