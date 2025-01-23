from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    order = models.Order()
    order.id = 12345
    order.pet_id = 98765
    order.quantity = 5
    order.ship_date = "2025-01-01T17:32:28Z"
    order.status = "approved"
    order.complete = False

    try:
        api_caller = api.StoreApi(api_client)

        response = api_caller.place_order(
            order=order,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Store#place_order: %s\n" % e)
