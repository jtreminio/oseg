using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class CreateUsersWithArrayInputDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.ApiKey = "YOUR_API_KEY";

        var user1 = new User(
            id: 12345,
            username: "my_user_1",
            firstName: "John",
            lastName: "Doe",
            email: "john@example.com",
            password: "secure_123",
            phone: "555-123-1234",
            userStatus: 1
        );

        var user2 = new User(
            id: 67890,
            username: "my_user_2",
            firstName: "Jane",
            lastName: "Doe",
            email: "jane@example.com",
            password: "secure_456",
            phone: "555-123-5678",
            userStatus: 2
        );

        var user = new List<User>
        {
            user1,
            user2,
        };

        try
        {
            new UserApi(config).CreateUsersWithArrayInput(
                user: user
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling User#CreateUsersWithArrayInput: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
