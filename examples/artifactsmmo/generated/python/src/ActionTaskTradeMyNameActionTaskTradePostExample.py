from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    simple_item_schema = models.SimpleItemSchema(
        code=None,
        quantity=None,
    )

    try:
        response = api.MyCharactersApi(api_client).action_task_trade_my_name_action_task_trade_post(
            name=None,
            simple_item_schema=simple_item_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_task_trade_my_name_action_task_trade_post: %s\n" % e)
