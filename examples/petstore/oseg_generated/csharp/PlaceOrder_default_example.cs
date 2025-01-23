using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class PlaceOrderDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        var order = new Order(
            id: 12345,
            petId: 98765,
            quantity: 5,
            shipDate: "2025-01-01T17:32:28Z",
            status: Order.StatusEnum.Approved,
            complete: false
        );

        try
        {
            var apiCaller = new StoreApi(config);

            var response = apiCaller.PlaceOrder(
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
