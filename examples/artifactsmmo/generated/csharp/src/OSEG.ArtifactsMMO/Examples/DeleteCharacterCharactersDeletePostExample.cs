using System;
using System.Collections.Generic;
using System.IO;

using Com.ArtifactsMMO.Api;
using Com.ArtifactsMMO.Client;
using Com.ArtifactsMMO.Model;

namespace OSEG.ArtifactsMMO.Examples;

public class DeleteCharacterCharactersDeletePostExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

        var deleteCharacterSchema = new DeleteCharacterSchema(
            name: null
        );

        try
        {
            var response = new CharactersApi(config).DeleteCharacterCharactersDeletePost(
                deleteCharacterSchema: deleteCharacterSchema
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Characters#DeleteCharacterCharactersDeletePost: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
