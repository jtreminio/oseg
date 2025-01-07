from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.PetApi(api_client)

        response = api_caller.find_pets_by_tags(
            tags=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#find_pets_by_tags: %s\n" % e)
