from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.UserApi(api_client)

        api_caller.delete_user(
            username=None,
        )
    except ApiException as e:
        print("Exception when calling User#delete_user: %s\n" % e)
