using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionGeCancelSellOrderMyNameActionGrandexchangeCancelPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var gECancelOrderSchema = new GECancelOrderSchema(
            id: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionGeCancelSellOrderMyNameActionGrandexchangeCancelPost(
                name: null,
                gECancelOrderSchema: gECancelOrderSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionGeCancelSellOrderMyNameActionGrandexchangeCancelPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
