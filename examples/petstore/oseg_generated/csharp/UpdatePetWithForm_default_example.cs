using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class UpdatePetWithFormDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            new PetApi(config).UpdatePetWithForm(
                petId: null,
                name: null,
                status: null
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
