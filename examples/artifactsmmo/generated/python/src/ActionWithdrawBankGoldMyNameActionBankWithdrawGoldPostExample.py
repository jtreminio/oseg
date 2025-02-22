from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    deposit_withdraw_gold_schema = models.DepositWithdrawGoldSchema(
        quantity=None,
    )

    try:
        response = api.MyCharactersApi(api_client).action_withdraw_bank_gold_my_name_action_bank_withdraw_gold_post(
            name=None,
            deposit_withdraw_gold_schema=deposit_withdraw_gold_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyCharacters#action_withdraw_bank_gold_my_name_action_bank_withdraw_gold_post: %s\n" % e)
