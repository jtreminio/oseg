using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class GetTicketCodeDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var apiCaller = new TicketsApi(config);

            var response = apiCaller.GetTicketCode(
                ticketId: "a54a57ca-36f8-421b-a6b4-2e8f26858a4c"
            );
            var fileStream = File.Create("file_response.zip");
            response.Seek(0, SeekOrigin.Begin);
            response.CopyTo(fileStream);
            fileStream.Close();
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Tickets#GetTicketCode: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
