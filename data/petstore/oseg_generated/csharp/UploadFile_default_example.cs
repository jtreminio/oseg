using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class UploadFileDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new PetApi(config);

            var response = apiCaller.UploadFile(
                petId: 12345,
                additionalMetadata: null,
                file: new FileStream(
                    path: "/path/to/file",
                    mode: FileMode.Open
                )
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#UploadFile: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
