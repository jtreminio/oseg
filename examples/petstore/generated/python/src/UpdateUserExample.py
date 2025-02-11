from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    api_key={"api_key": "YOUR_API_KEY"},
)

with ApiClient(configuration) as api_client:
    user = models.User(
        id=12345,
        username="new-username",
        firstName="Joe",
        lastName="Broke",
        email="some-email@example.com",
        password="so secure omg",
        phone="555-867-5309",
        userStatus=1,
    )

    try:
        api.UserApi(api_client).update_user(
            username="my-username",
            user=user,
        )
    except ApiException as e:
        print("Exception when calling User#update_user: %s\n" % e)
