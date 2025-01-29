from datetime import date, datetime
from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    buy_museum_tickets = models.BuyMuseumTickets(
        ticket_type="event",
        ticket_date=date.fromisoformat("2023-09-05"),
        email="todd@example.com",
        ticket_id=None,
        event_id="dad4bce8-f5cb-4078-a211-995864315e39",
    )

    try:
        response = api.TicketsApi(api_client).buy_museum_tickets(
            buy_museum_tickets=buy_museum_tickets,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Tickets#buy_museum_tickets: %s\n" % e)
