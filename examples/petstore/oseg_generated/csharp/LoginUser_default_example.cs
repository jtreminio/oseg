using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class LoginUserDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var response = new UserApi(config).LoginUser(
                username: "my_username",
                password: "my_secret_password"
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling User#LoginUser: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
