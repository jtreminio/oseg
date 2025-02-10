using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class DeleteUserDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.ApiKey = "YOUR_API_KEY";

        try
        {
            new UserApi(config).DeleteUser(
                username: "my_username"
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling User#DeleteUser: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
