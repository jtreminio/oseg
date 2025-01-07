using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class DeleteOrderDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new StoreApi(config);

            apiCaller.DeleteOrder(
                orderId: null
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
