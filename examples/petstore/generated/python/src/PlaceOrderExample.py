from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    order = models.Order(
        id=12345,
        petId=98765,
        quantity=5,
        shipDate=datetime.fromisoformat("2025-01-01T17:32:28Z"),
        status="approved",
        complete=False,
    )

    try:
        response = api.StoreApi(api_client).place_order(
            order=order,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Store#place_order: %s\n" % e)
