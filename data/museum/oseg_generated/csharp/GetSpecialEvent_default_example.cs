using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class GetSpecialEventDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new EventsApi(config);

            var response = apiCaller.GetSpecialEvent(
                eventId: "dad4bce8-f5cb-4078-a211-995864315e39"
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Events#GetSpecialEvent: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
