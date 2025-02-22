using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionNpcBuyItemMyNameActionNpcBuyPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var npcMerchantBuySchema = new NpcMerchantBuySchema(
            code: null,
            quantity: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionNpcBuyItemMyNameActionNpcBuyPost(
                name: null,
                npcMerchantBuySchema: npcMerchantBuySchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionNpcBuyItemMyNameActionNpcBuyPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
