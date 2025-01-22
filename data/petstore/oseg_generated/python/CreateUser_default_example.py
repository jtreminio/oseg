from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    user = models.User()
    user.id = 12345
    user.username = "my_user"
    user.first_name = "John"
    user.last_name = "Doe"
    user.email = "john@example.com"
    user.password = "secure_123"
    user.phone = "555-123-1234"
    user.user_status = 1

    try:
        api_caller = api.UserApi(api_client)

        api_caller.create_user(
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#create_user: %s\n" % e)
