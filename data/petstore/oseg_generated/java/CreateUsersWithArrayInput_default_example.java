package org.openapitools.client.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class CreateUsersWithArrayInput_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var user1 = new User()
            .id(12345L)
            .username("my_user")
            .firstName("John")
            .lastName("Doe")
            .email("john@example.com")
            .password("secure_123")
            .phone("555-123-1234")
            .userStatus(1);

        var user2 = new User()
            .id(12345L)
            .username("my_user")
            .firstName("John")
            .lastName("Doe")
            .email("john@example.com")
            .password("secure_123")
            .phone("555-123-1234")
            .userStatus(1);

        var user = List.of (
            user1,
            user2
        );

        try
        {
            var apiCaller = new UserApi(config);

            apiCaller.createUsersWithArrayInput(
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
