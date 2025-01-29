from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event = models.SpecialEvent(
        name="Mermaid Treasure Identification and Analysis",
        location="Under the seaaa 🦀 🎶 🌊.",
        event_description="Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
        price=0,
        dates=[
            date.fromisoformat("2023-09-05"),
            date.fromisoformat("2023-09-08"),
        ],
        event_id=None,
    )

    try:
        response = api.EventsApi(api_client).create_special_event(
            special_event=special_event,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#create_special_event: %s\n" % e)
