import * as fs from 'fs';
import * as apis from "openapimuseum_client/api/apis"
import * as models from "openapimuseum_client/model/models"

const apiCaller = new apis.TicketsApi();

const ticketId = "a54a57ca-36f8-421b-a6b4-2e8f26858a4c";

apiCaller.getTicketCode(
    ticketId,
).then(response => {
  fs.createWriteStream('file_response.zip').write(response.body);
}).catch(error => {
  console.log("Exception when calling Tickets#getTicketCode:");
  console.log(error.body);
});
