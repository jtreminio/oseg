using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionWithdrawBankMyNameActionBankWithdrawPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var simpleItemSchema = new SimpleItemSchema(
            code: null,
            quantity: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionWithdrawBankMyNameActionBankWithdrawPost(
                name: null,
                simpleItemSchema: simpleItemSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionWithdrawBankMyNameActionBankWithdrawPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
