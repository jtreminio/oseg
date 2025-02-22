from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.MyAccountApi(api_client).get_ge_sell_history_my_grandexchange_history_get(
            id=None,
            code=None,
            page=1,
            size=50,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyAccount#get_ge_sell_history_my_grandexchange_history_get: %s\n" % e)
