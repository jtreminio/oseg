using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class BuyMuseumTicketsEventEntry
{
    public static void Main()
    {
        var config = new Configuration();

        var buyMuseumTickets = new BuyMuseumTickets(
            ticketType: BuyMuseumTickets.TicketTypeEnum.Event,
            ticketDate: DateOnly.Parse("2023-09-05"),
            email: "todd@example.com",
            ticketId: null,
            eventId: "dad4bce8-f5cb-4078-a211-995864315e39"
        );

        try
        {
            var response = new TicketsApi(config).BuyMuseumTickets(
                buyMuseumTickets: buyMuseumTickets
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Tickets#BuyMuseumTickets: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
