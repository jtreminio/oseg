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
            name: "Mermaid Treasure Identification and Analysis",
            location: "Under the seaaa 🦀 🎶 🌊.",
            eventDescription: "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.",
            price: 0,
            eventId: null
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
