package org.openapimuseum.client.examples;

import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.api.*;
import org.openapimuseum.client.auth.*;
import org.openapimuseum.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class BuyMuseumTickets_general_entry
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var buyMuseumTickets = new BuyMuseumTickets()
            .ticketType(BuyMuseumTickets.TicketTypeEnum.GENERAL)
            .ticketDate("2023-09-07")
            .email("todd@example.com")
            .ticketId(null)
            .eventId(null);

        try
        {
            var apiCaller = new TicketsApi(config);

            var response = apiCaller.buyMuseumTickets(
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
