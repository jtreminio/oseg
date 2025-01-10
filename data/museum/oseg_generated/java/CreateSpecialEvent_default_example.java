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
            .name("Mermaid Treasure Identification and Analysis")
            .location("Under the seaaa 🦀 🎶 🌊.")
            .eventDescription("Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel.")
            .price(0F)
            .eventId(null);

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
