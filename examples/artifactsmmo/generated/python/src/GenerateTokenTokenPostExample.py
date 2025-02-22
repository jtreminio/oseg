from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.TokenApi(api_client).generate_token_token_post()

        pprint(response)
    except ApiException as e:
        print("Exception when calling Token#generate_token_token_post: %s\n" % e)
