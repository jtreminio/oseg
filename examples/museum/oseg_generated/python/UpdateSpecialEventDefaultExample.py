from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event_fields = models.SpecialEventFields(
        name=None,
        location="On the beach.",
        event_description=None,
        price=15,
        dates=None,
    )

    try:
        response = api.EventsApi(api_client).update_special_event(
            event_id="dad4bce8-f5cb-4078-a211-995864315e39",
            special_event_fields=special_event_fields,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#update_special_event: %s\n" % e)
