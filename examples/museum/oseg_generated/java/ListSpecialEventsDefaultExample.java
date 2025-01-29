package org.openapimuseum.client.examples;

import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.api.*;
import org.openapimuseum.client.auth.*;
import org.openapimuseum.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;

public class ListSpecialEvents_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        try
        {
            var response = new EventsApi(config).listSpecialEvents(
                LocalDate.parse("2023-02-23"),
                LocalDate.parse("2023-04-18"),
                2,
                15
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Events#listSpecialEvents");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
