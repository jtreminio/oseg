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

public class CreateUserDefaultExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setApiKey("YOUR_API_KEY");

        var user = new User();
        user.id(12345L);
        user.username("my_user");
        user.firstName("John");
        user.lastName("Doe");
        user.email("john@example.com");
        user.password("secure_123");
        user.phone("555-123-1234");
        user.userStatus(1);

        try
        {
            new UserApi(config).createUser(
                user
            );
        } catch (ApiException e) {
            System.err.println("Exception when calling User#createUser");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
