using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class ActionMoveMyNameActionMovePostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var destinationSchema = new DestinationSchema(
            x: null,
            y: null
        );

        try
        {
            var response = new MyCharactersApi(config).ActionMoveMyNameActionMovePost(
                name: null,
                destinationSchema: destinationSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling MyCharacters#ActionMoveMyNameActionMovePost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
