using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class PlaceOrderExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";
        // config.ApiKey = "YOUR_API_KEY";

        var order = new Order(
            id: 12345,
            petId: 98765,
            quantity: 5,
            shipDate: DateTime.Parse("2025-01-01T17:32:28Z"),
            status: Order.StatusEnum.Approved,
            complete: false
        );

        try
        {
            var response = new StoreApi(config).PlaceOrder(
                order: order
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Store#PlaceOrder: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
