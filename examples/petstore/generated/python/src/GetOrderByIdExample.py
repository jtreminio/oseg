from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    try:
        response = api.StoreApi(api_client).get_order_by_id(
            order_id=3,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Store#get_order_by_id: %s\n" % e)
