package org.openapitools.client.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.Map;

public class GetOrderById_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        try
        {
            var response = new StoreApi(config).getOrderById(
                3L
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Store#getOrderById");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
