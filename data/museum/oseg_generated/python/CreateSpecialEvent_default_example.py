from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event = models.SpecialEvent()
    special_event.name = "Pirate Coding Workshop"
    special_event.location = "Computer Room"
    special_event.eventDescription = "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang)."
    special_event.price = 25
    special_event.dates = [
        "2023-09-05",
        "2023-09-08",
    ]
    special_event.eventId = "3be6453c-03eb-4357-ae5a-984a0e574a54"

    try:
        api_caller = api.EventsApi(api_client)

        response = api_caller.create_special_event(
            special_event=special_event,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#create_special_event: %s\n" % e)
