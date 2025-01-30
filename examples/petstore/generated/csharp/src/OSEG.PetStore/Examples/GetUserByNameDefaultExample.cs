using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class GetUserByNameDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();

        try
        {
            var response = new UserApi(config).GetUserByName(
                username: "my_username"
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling User#GetUserByName: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
