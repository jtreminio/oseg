using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class FindPetsByStatusDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var response = new PetApi(config).FindPetsByStatus(
                status: [
                    "available",
                    "pending",
                ]
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#FindPetsByStatus: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
