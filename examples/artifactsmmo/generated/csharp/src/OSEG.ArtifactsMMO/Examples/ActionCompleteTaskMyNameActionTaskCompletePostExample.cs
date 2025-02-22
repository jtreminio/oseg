using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionCompleteTaskMyNameActionTaskCompletePostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        try
        {
            var response = new MyCharactersApi(config).ActionCompleteTaskMyNameActionTaskCompletePost(
                name: null
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionCompleteTaskMyNameActionTaskCompletePost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
