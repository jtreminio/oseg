using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionGeCreateSellOrderMyNameActionGrandexchangeSellPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var gEOrderCreationrSchema = new GEOrderCreationrSchema(
            code: null,
            quantity: null,
            price: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionGeCreateSellOrderMyNameActionGrandexchangeSellPost(
                name: null,
                gEOrderCreationrSchema: gEOrderCreationrSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionGeCreateSellOrderMyNameActionGrandexchangeSellPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
