package org.openapitools.client.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class PlaceOrder_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var order = new Order()
            .id(12345L)
            .petId(98765L)
            .quantity(5)
            .shipDate("2025-01-01T17:32:28Z")
            .status(Order.StatusEnum.APPROVED)
            .complete(false);

        try
        {
            var apiCaller = new StoreApi(config);

            var response = apiCaller.placeOrder(
                order
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Store#placeOrder");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
