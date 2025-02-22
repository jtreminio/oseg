from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.MyAccountApi(api_client).get_bank_details_my_bank_get()

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyAccount#get_bank_details_my_bank_get: %s\n" % e)
