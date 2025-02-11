using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class CreateUserExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.ApiKey = "YOUR_API_KEY";

        var user = new User(
            id: 12345,
            username: "my_user",
            firstName: "John",
            lastName: "Doe",
            email: "john@example.com",
            password: "secure_123",
            phone: "555-123-1234",
            userStatus: 1
        );

        try
        {
            new UserApi(config).CreateUser(
                user: user
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling User#CreateUser: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
