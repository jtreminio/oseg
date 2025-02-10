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

public class CreateUsersWithArrayInputDefaultExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setApiKey("YOUR_API_KEY");

        var user1 = new User();
        user1.id(12345L);
        user1.username("my_user_1");
        user1.firstName("John");
        user1.lastName("Doe");
        user1.email("john@example.com");
        user1.password("secure_123");
        user1.phone("555-123-1234");
        user1.userStatus(1);

        var user2 = new User();
        user2.id(67890L);
        user2.username("my_user_2");
        user2.firstName("Jane");
        user2.lastName("Doe");
        user2.email("jane@example.com");
        user2.password("secure_456");
        user2.phone("555-123-5678");
        user2.userStatus(2);

        var user = new ArrayList<User>(List.of (
            user1,
            user2
        ));

        try
        {
            new UserApi(config).createUsersWithArrayInput(
                user
            );
        } catch (ApiException e) {
            System.err.println("Exception when calling User#createUsersWithArrayInput");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
