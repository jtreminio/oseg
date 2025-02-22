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
        response = api.ItemsApi(api_client).get_all_items_items_get(
            min_level=None,
            max_level=None,
            name=None,
            type=None,
            craft_skill=None,
            craft_material=None,
            page=1,
            size=50,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Items#get_all_items_items_get: %s\n" % e)
