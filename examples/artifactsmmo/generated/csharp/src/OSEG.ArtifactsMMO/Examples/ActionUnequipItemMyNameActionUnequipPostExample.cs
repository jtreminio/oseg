using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionUnequipItemMyNameActionUnequipPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var unequipSchema = new UnequipSchema(
            slot: null,
            quantity: 1
        );

        try
        {
            var response = new MyCharactersApi(config).ActionUnequipItemMyNameActionUnequipPost(
                name: null,
                unequipSchema: unequipSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionUnequipItemMyNameActionUnequipPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
