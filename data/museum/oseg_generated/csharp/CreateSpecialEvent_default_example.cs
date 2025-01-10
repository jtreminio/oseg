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
