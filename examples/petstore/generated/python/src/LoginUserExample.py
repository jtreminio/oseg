from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    try:
        response = api.UserApi(api_client).login_user(
            username="my_username",
            password="my_secret_password",
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling User#login_user: %s\n" % e)
