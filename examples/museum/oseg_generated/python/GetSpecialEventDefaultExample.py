from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        response = api.EventsApi(api_client).get_special_event(
            event_id="dad4bce8-f5cb-4078-a211-995864315e39",
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#get_special_event: %s\n" % e)
