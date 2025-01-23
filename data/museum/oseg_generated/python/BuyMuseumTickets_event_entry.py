from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    buy_museum_tickets = models.BuyMuseumTickets()
    buy_museum_tickets.ticket_type = "event"
    buy_museum_tickets.ticket_date = "2023-09-05"
    buy_museum_tickets.email = "todd@example.com"
    buy_museum_tickets.ticket_id = None
    buy_museum_tickets.event_id = "dad4bce8-f5cb-4078-a211-995864315e39"

    try:
        api_caller = api.TicketsApi(api_client)

        response = api_caller.buy_museum_tickets(
            buy_museum_tickets=buy_museum_tickets,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Tickets#buy_museum_tickets: %s\n" % e)
