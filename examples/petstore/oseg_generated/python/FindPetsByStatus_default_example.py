from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        response = api.PetApi(api_client).find_pets_by_status(
            status=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#find_pets_by_status: %s\n" % e)
