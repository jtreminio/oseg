using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class GetInventoryDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new StoreApi(config);

            var response = apiCaller.GetInventory();

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Store#GetInventory: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
