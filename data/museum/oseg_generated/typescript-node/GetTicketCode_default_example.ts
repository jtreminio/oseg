import * as fs from 'fs';
import * as openapimuseum_client from "openapimuseum_client";

const apiCaller = new openapimuseum_client.TicketsApi();

const ticketId = "a54a57ca-36f8-421b-a6b4-2e8f26858a4c";
apiCaller.getTicketCode(
    ticketId,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#getTicketCode:");
  console.log(error.body);
});
