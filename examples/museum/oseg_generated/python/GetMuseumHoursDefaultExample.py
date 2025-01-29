from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        response = api.OperationsApi(api_client).get_museum_hours(
            start_date=date.fromisoformat("2023-02-23"),
            page=2,
            limit=15,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Operations#get_museum_hours: %s\n" % e)
