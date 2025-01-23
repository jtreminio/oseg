from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.OperationsApi(api_client)

        response = api_caller.get_museum_hours(
            start_date="2023-02-23",
            page=2,
            limit=15,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Operations#get_museum_hours: %s\n" % e)
