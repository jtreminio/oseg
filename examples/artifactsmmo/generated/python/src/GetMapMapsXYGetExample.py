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
        response = api.MapsApi(api_client).get_map_maps_x__y_get(
            x=None,
            y=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Maps#get_map_maps_x__y_get: %s\n" % e)
