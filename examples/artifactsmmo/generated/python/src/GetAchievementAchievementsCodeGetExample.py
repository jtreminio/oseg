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
        response = api.AchievementsApi(api_client).get_achievement_achievements_code_get(
            code=None,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Achievements#get_achievement_achievements_code_get: %s\n" % e)
