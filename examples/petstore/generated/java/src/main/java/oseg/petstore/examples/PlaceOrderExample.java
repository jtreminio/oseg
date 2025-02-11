package oseg.petstore.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class PlaceOrderExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setAccessToken("YOUR_ACCESS_TOKEN");
        // config.setApiKey("YOUR_API_KEY");

        var order = new Order();
        order.id(12345L);
        order.petId(98765L);
        order.quantity(5);
        order.shipDate(OffsetDateTime.parse("2025-01-01T17:32:28Z"));
        order.status(Order.StatusEnum.APPROVED);
        order.complete(false);

        try
        {
            var response = new StoreApi(config).placeOrder(
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
