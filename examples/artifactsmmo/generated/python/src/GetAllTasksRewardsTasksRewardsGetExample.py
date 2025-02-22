from datetime import date, datetime
from pprint import pprint

from artifacts_mmo_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
    # username=# "YOUR_USERNAME",
    # password=# "YOUR_PASSWORD",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.TasksApi(api_client).get_all_tasks_rewards_tasks_rewards_get(
            page=1,
            size=50,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Tasks#get_all_tasks_rewards_tasks_rewards_get: %s\n" % e)
