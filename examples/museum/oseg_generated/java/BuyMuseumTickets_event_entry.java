package org.openapimuseum.client.examples;

import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.api.*;
import org.openapimuseum.client.auth.*;
import org.openapimuseum.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;

public class BuyMuseumTickets_event_entry
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var buyMuseumTickets = new BuyMuseumTickets()
            .ticketType(BuyMuseumTickets.TicketTypeEnum.EVENT)
            .ticketDate(LocalDate.parse("2023-09-05"))
            .email("todd@example.com")
            .ticketId(null)
            .eventId("dad4bce8-f5cb-4078-a211-995864315e39");

        try
        {
            var response = new TicketsApi(config).buyMuseumTickets(
                buyMuseumTickets
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Tickets#buyMuseumTickets");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
