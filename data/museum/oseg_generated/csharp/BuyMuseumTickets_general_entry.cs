using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class BuyMuseumTicketsGeneralEntry
{
    public static void Main()
    {
        var config = new Configuration();

        var buyMuseumTickets = new BuyMuseumTickets(
            ticketType: BuyMuseumTickets.TicketTypeEnum.General,
            ticketDate: "2023-09-07",
            email: "todd@example.com",
            ticketId: null,
            eventId: null
        );

        try
        {
            var apiCaller = new TicketsApi(config);

            var response = apiCaller.BuyMuseumTickets(
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
