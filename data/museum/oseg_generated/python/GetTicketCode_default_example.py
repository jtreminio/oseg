from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.TicketsApi(api_client)

        response = api_caller.get_ticket_code(
            ticket_id="a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Tickets#get_ticket_code: %s\n" % e)
