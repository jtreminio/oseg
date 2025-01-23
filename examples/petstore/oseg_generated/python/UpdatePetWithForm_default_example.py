from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.PetApi(api_client)

        api_caller.update_pet_with_form(
            pet_id=None,
            name=None,
            status=None,
        )
    except ApiException as e:
        print("Exception when calling Pet#update_pet_with_form: %s\n" % e)
