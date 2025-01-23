from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    user_1 = models.User()
    user_1.id = 12345
    user_1.username = "my_user"
    user_1.first_name = "John"
    user_1.last_name = "Doe"
    user_1.email = "john@example.com"
    user_1.password = "secure_123"
    user_1.phone = "555-123-1234"
    user_1.user_status = 1

    user_2 = models.User()
    user_2.id = 12345
    user_2.username = "my_user"
    user_2.first_name = "John"
    user_2.last_name = "Doe"
    user_2.email = "john@example.com"
    user_2.password = "secure_123"
    user_2.phone = "555-123-1234"
    user_2.user_status = 1

    user = [
        user_1,
        user_2,
    ]

    try:
        api_caller = api.UserApi(api_client)

        api_caller.create_users_with_array_input(
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#create_users_with_array_input: %s\n" % e)
