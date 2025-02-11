from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        api.PetApi(api_client).update_pet_with_form(
            pet_id=12345,
            name="Pet's new name",
            status="sold",
        )
    except ApiException as e:
        print("Exception when calling Pet#update_pet_with_form: %s\n" % e)
