from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    user = models.User()
    user.id = 12345
    user.username = "new-username"
    user.first_name = "Joe"
    user.last_name = "Broke"
    user.email = "some-email@example.com"
    user.password = "so secure omg"
    user.phone = "555-867-5309"
    user.user_status = 1

    try:
        api_caller = api.UserApi(api_client)

        api_caller.update_user(
            username="my-username",
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#update_user: %s\n" % e)
