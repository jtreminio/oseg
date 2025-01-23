from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event = models.SpecialEvent()
    special_event.name = "Mermaid Treasure Identification and Analysis"
    special_event.location = "Under the seaaa 🦀 🎶 🌊."
    special_event.event_description = "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel."
    special_event.price = 0
    special_event.dates = [
        "2023-09-05",
        "2023-09-08",
    ]
    special_event.event_id = None

    try:
        api_caller = api.EventsApi(api_client)

        response = api_caller.create_special_event(
            special_event=special_event,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#create_special_event: %s\n" % e)
