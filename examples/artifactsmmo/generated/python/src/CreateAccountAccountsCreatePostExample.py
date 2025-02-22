from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # username=# "YOUR_USERNAME",
    # password=# "YOUR_PASSWORD",
)

with ApiClient(configuration) as api_client:
    add_account_schema = models.AddAccountSchema(
        username=None,
        password=None,
        email=None,
    )

    try:
        response = api.AccountsApi(api_client).create_account_accounts_create_post(
            add_account_schema=add_account_schema,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Accounts#create_account_accounts_create_post: %s\n" % e)
