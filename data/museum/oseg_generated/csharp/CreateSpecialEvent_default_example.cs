using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class CreateSpecialEventDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        var specialEvent = new SpecialEvent(
            name: "Pirate Coding Workshop",
            location: "Computer Room",
            eventDescription: "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).",
            price: 25,
            dates: new List<string>
            {
                "2023-09-05",
                "2023-09-08"
            },
            eventId: "3be6453c-03eb-4357-ae5a-984a0e574a54"
        );

        try
        {
            var apiCaller = new EventsApi(config);

            var response = apiCaller.CreateSpecialEvent(
                specialEvent: specialEvent
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Events#CreateSpecialEvent: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
