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
        response = api.MapsApi(api_client).get_all_maps_maps_get(
            content_type=None,
            content_code=None,
            page=1,
            size=50,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Maps#get_all_maps_maps_get: %s\n" % e)
