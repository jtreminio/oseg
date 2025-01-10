from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    special_event = models.SpecialEvent()

    try:
        api_caller = api.EventsApi(api_client)

        response = api_caller.create_special_event(
            special_event=special_event,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#create_special_event: %s\n" % e)
