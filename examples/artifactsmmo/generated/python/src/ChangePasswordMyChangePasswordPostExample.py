from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    change_password = models.ChangePassword(
        currentPassword=None,
        newPassword=None,
    )

    try:
        response = api.MyAccountApi(api_client).change_password_my_change_password_post(
            change_password=change_password,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling MyAccount#change_password_my_change_password_post: %s\n" % e)
