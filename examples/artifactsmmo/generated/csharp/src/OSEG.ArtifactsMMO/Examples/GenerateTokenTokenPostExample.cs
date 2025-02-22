using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class GenerateTokenTokenPostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.Username = "YOUR_USERNAME";
        config.Password = "YOUR_PASSWORD";

        try
        {
            var response = new TokenApi(config).GenerateTokenTokenPost();

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Token#GenerateTokenTokenPost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
