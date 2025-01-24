from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    user_1 = models.User(
        id=12345,
        username="my_user",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="secure_123",
        phone="555-123-1234",
        user_status=1,
    )

    user_2 = models.User(
        id=12345,
        username="my_user",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="secure_123",
        phone="555-123-1234",
        user_status=1,
    )

    user = [
        user_1,
        user_2,
    ]

    try:
        api.UserApi(api_client).create_users_with_list_input(
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#create_users_with_list_input: %s\n" % e)
