from pprint import pprint

from openapimuseum_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    buy_museum_tickets = models.BuyMuseumTickets()
    buy_museum_tickets.email = "todd@example.com"
    buy_museum_tickets.ticketId = None
    buy_museum_tickets.ticketDate = "2023-09-07"
    buy_museum_tickets.ticketType = "general"
    buy_museum_tickets.eventId = None

    try:
        api_caller = api.TicketsApi(api_client)

        response = api_caller.buy_museum_tickets(
            buy_museum_tickets=buy_museum_tickets,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Tickets#buy_museum_tickets: %s\n" % e)
