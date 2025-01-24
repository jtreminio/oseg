import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.TicketsApi();

const buyMuseumTickets = new models.BuyMuseumTickets();
buyMuseumTickets.ticketType = models.BuyMuseumTickets.TicketTypeEnum.General;
buyMuseumTickets.ticketDate = "2023-09-07";
buyMuseumTickets.email = "todd@example.com";
buyMuseumTickets.ticketId = undefined;
buyMuseumTickets.eventId = undefined;

apiCaller.buyMuseumTickets(
    buyMuseumTickets,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#buyMuseumTickets:");
  console.log(error.body);
});
