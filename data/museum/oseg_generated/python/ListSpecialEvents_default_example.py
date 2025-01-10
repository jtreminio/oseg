from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.EventsApi(api_client)

        response = api_caller.list_special_events(
            start_date="2023-02-23",
            end_date="2023-04-18",
            page=2,
            limit=15,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Events#list_special_events: %s\n" % e)
