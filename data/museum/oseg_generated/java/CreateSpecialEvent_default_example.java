package org.openapimuseum.client.examples;

import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.api.*;
import org.openapimuseum.client.auth.*;
import org.openapimuseum.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class CreateSpecialEvent_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var specialEvent = new SpecialEvent()
            .name("Pirate Coding Workshop")
            .location("Computer Room")
            .eventDescription("Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang).")
            .price(25F)
            .dates(List.of (
                "2023-09-05",
                "2023-09-08"
            ))
            .eventId("3be6453c-03eb-4357-ae5a-984a0e574a54");

        try
        {
            var apiCaller = new EventsApi(config);

            var response = apiCaller.createSpecialEvent(
                specialEvent
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Events#createSpecialEvent");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
