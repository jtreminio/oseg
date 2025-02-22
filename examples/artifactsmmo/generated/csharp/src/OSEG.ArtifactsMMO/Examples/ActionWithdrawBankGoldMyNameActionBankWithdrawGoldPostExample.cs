using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionWithdrawBankGoldMyNameActionBankWithdrawGoldPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var depositWithdrawGoldSchema = new DepositWithdrawGoldSchema(
            quantity: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionWithdrawBankGoldMyNameActionBankWithdrawGoldPost(
                name: null,
                depositWithdrawGoldSchema: depositWithdrawGoldSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionWithdrawBankGoldMyNameActionBankWithdrawGoldPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
