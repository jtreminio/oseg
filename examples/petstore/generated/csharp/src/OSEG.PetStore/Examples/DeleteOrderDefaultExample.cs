using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class DeleteOrderDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";
        config.ApiKey = "YOUR_API_KEY";

        try
        {
            new StoreApi(config).DeleteOrder(
                orderId: "12345"
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Store#DeleteOrder: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
