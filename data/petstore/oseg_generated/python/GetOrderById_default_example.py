from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.StoreApi(api_client)

        response = api_caller.get_order_by_id(
            order_id=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Store#get_order_by_id: %s\n" % e)
