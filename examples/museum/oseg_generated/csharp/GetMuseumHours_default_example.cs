using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPIMuseum.Api;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

public class GetMuseumHoursDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        try
        {
            var response = new OperationsApi(config).GetMuseumHours(
                startDate: DateOnly.Parse("2023-02-23"),
                page: 2,
                limit: 15
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Operations#GetMuseumHours: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
