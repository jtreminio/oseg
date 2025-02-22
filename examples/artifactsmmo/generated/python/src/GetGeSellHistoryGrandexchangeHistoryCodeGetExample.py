from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # username=# "YOUR_USERNAME",
    # password=# "YOUR_PASSWORD",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.GrandExchangeApi(api_client).get_ge_sell_history_grandexchange_history_code_get(
            code=None,
            seller=None,
            buyer=None,
            page=1,
            size=50,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling GrandExchange#get_ge_sell_history_grandexchange_history_code_get: %s\n" % e)
