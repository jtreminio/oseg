using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class GetAllActiveEventsEventsActiveGetExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";
        // config.Username = "YOUR_USERNAME";
        // config.Password = "YOUR_PASSWORD";

        try
        {
            var response = new EventsApi(config).GetAllActiveEventsEventsActiveGet(
                page: 1,
                size: 50
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Events#GetAllActiveEventsEventsActiveGet: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
