import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.TicketsApi();

const buy_museum_tickets: openapimuseum_client.BuyMuseumTickets = {
    ticketType: openapimuseum_client.BuyMuseumTickets.TicketTypeEnum.General,
    ticketDate: "2023-09-07",
    email: "todd@example.com",
    ticketId: undefined,
    eventId: undefined,
};

apiCaller.buyMuseumTickets(
    buyMuseumTickets,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#buyMuseumTickets:");
  console.log(error.body);
});
