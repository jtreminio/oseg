using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class GetOrderByIdDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";
        // config.ApiKey = "YOUR_API_KEY";

        try
        {
            var response = new StoreApi(config).GetOrderById(
                orderId: 3
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Store#GetOrderById: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
