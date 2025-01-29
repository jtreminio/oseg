import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.TicketsApi();

const buyMuseumTickets = new models.BuyMuseumTickets();
buyMuseumTickets.ticketType = models.BuyMuseumTickets.TicketTypeEnum.Event;
buyMuseumTickets.ticketDate = "2023-09-05";
buyMuseumTickets.email = "todd@example.com";
buyMuseumTickets.ticketId = undefined;
buyMuseumTickets.eventId = "dad4bce8-f5cb-4078-a211-995864315e39";

apiCaller.buyMuseumTickets(
    buyMuseumTickets,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#buyMuseumTickets:");
  console.log(error.body);
});
