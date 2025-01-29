using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class DeletePetDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();

        try
        {
            new PetApi(config).DeletePet(
                petId: 12345,
                apiKey: "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a"
            );
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#DeletePet: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
