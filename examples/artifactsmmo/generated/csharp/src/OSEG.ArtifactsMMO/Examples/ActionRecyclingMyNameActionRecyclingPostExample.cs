using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionRecyclingMyNameActionRecyclingPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var recyclingSchema = new RecyclingSchema(
            code: null,
            quantity: 1
        );

        try
        {
            var response = new MyCharactersApi(config).ActionRecyclingMyNameActionRecyclingPost(
                name: null,
                recyclingSchema: recyclingSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionRecyclingMyNameActionRecyclingPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
