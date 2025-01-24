from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        response = api.UserApi(api_client).get_user_by_name(
            username=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling User#get_user_by_name: %s\n" % e)
