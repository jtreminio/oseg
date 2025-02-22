from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    ge_cancel_order_schema = models.GECancelOrderSchema(
        id=None,
    )

    try:
        response = api.MyCharactersApi(api_client).action_ge_cancel_sell_order_my_name_action_grandexchange_cancel_post(
            name=None,
            ge_cancel_order_schema=ge_cancel_order_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_ge_cancel_sell_order_my_name_action_grandexchange_cancel_post: %s\n" % e)
