package org.openapitools.client.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class UpdateUser_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var user = new User()
            .id(12345L)
            .username("new-username")
            .firstName("Joe")
            .lastName("Broke")
            .email("some-email@example.com")
            .password("so secure omg")
            .phone("555-867-5309")
            .userStatus(1);

        try
        {
            var apiCaller = new UserApi(config);

            apiCaller.updateUser(
                "my-username",
                user
            );
        } catch (ApiException e) {
            System.err.println("Exception when calling User#updateUser");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
