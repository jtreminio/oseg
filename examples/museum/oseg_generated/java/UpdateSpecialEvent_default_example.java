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

public class UpdateSpecialEvent_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var specialEventFields = new SpecialEventFields()
            .name(null)
            .location("On the beach.")
            .eventDescription(null)
            .price(15F)
            .dates(null);

        try
        {
            var response = new EventsApi(config).updateSpecialEvent(
                "dad4bce8-f5cb-4078-a211-995864315e39",
                specialEventFields
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Events#updateSpecialEvent");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
