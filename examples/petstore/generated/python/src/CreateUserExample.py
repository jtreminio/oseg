from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    user = models.User(
        id=12345,
        username="my_user",
        firstName="John",
        lastName="Doe",
        email="john@example.com",
        password="secure_123",
        phone="555-123-1234",
        userStatus=1,
    )

    try:
        api.UserApi(api_client).create_user(
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#create_user: %s\n" % e)
