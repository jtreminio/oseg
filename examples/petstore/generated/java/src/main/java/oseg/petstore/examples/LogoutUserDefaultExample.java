package oseg.petstore.examples;

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

public class LogoutUserDefaultExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        try
        {
            new UserApi(config).logoutUser();
        } catch (ApiException e) {
            System.err.println("Exception when calling User#logoutUser");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
