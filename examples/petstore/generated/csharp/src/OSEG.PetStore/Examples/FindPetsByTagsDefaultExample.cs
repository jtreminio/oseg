using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStore.Examples;

public class FindPetsByTagsDefaultExample
{
    public static void Run()
    {
        var config = new Configuration();

        try
        {
            var response = new PetApi(config).FindPetsByTags(
                tags: [
                    "tag_1",
                    "tag_2",
                ]
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#FindPetsByTags: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
