using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class UpdatePetWithFormExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        try
        {
            new PetApi(config).UpdatePetWithForm(
                petId: 12345,
                name: "Pet's new name",
                status: "sold"
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#UpdatePetWithForm: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
