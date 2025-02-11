from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    try:
        response = api.PetApi(api_client).get_pet_by_id(
            pet_id=12345,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#get_pet_by_id: %s\n" % e)
