from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    try:
        api.UserApi(api_client).logout_user()
    except ApiException as e:
        print("Exception when calling User#logout_user: %s\n" % e)
