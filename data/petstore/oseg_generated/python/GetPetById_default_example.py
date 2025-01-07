from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.PetApi(api_client)

        response = api_caller.get_pet_by_id(
            pet_id=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#get_pet_by_id: %s\n" % e)
