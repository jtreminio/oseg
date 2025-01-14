from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.StoreApi(api_client)

        api_caller.delete_order(
            order_id=None,
        )
    except ApiException as e:
        print("Exception when calling Store#delete_order: %s\n" % e)
