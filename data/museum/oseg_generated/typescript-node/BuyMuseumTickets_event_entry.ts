import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.TicketsApi();

const buyMuseumTickets: openapimuseum_client.BuyMuseumTickets = {
    ticketType: openapimuseum_client.BuyMuseumTickets.TicketTypeEnum.Event,
    ticketDate: "2023-09-05",
    email: "todd@example.com",
    ticketId: undefined,
    eventId: "dad4bce8-f5cb-4078-a211-995864315e39",
};

apiCaller.buyMuseumTickets(
    buyMuseumTickets,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#buyMuseumTickets:");
  console.log(error.body);
});
