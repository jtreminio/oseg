package org.openapimuseum.client.examples;

import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.api.*;
import org.openapimuseum.client.auth.*;
import org.openapimuseum.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class GetTicketCode_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        try
        {
            var apiCaller = new TicketsApi(config);

            var response = apiCaller.getTicketCode(
                "a54a57ca-36f8-421b-a6b4-2e8f26858a4c"
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Tickets#getTicketCode");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
