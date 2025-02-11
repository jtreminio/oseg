from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    try:
        api.StoreApi(api_client).delete_order(
            order_id="12345",
        )
    except ApiException as e:
        print("Exception when calling Store#delete_order: %s\n" % e)
