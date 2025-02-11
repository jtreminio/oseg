from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        api.PetApi(api_client).delete_pet(
            pet_id=12345,
            api_key="df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a",
        )
    except ApiException as e:
        print("Exception when calling Pet#delete_pet: %s\n" % e)
