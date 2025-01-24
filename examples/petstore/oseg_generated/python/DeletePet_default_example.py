from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api.PetApi(api_client).delete_pet(
            pet_id=None,
            api_key=None,
        )
    except ApiException as e:
        print("Exception when calling Pet#delete_pet: %s\n" % e)
