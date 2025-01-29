from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        response = api.TicketsApi(api_client).get_ticket_code(
            ticket_id="a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
        )

        open("file_response.zip", "wb").write(response.read())
    except ApiException as e:
        print("Exception when calling Tickets#get_ticket_code: %s\n" % e)
