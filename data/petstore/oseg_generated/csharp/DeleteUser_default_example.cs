using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class DeleteUserDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new UserApi(config);

            apiCaller.DeleteUser(
                username: null
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
