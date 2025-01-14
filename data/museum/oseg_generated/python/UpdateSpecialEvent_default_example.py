from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event_fields = models.SpecialEventFields()
    special_event_fields.name = None
    special_event_fields.location = "On the beach."
    special_event_fields.eventDescription = None
    special_event_fields.price = 15

    try:
        api_caller = api.EventsApi(api_client)

        response = api_caller.update_special_event(
            event_id="dad4bce8-f5cb-4078-a211-995864315e39",
            special_event_fields=special_event_fields,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#update_special_event: %s\n" % e)
