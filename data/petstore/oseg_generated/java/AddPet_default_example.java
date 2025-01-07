package org.openapitools.client.examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.model.*;

import java.io.File;
import java.util.List;
import java.util.Map;

public class AddPet_default_example
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();

        var category = new Category()
            .id(12345L)
            .name("Category_Name");

        var tags1 = new Tag()
            .id(12345L)
            .name("tag_1");

        var tags2 = new Tag()
            .id(98765L)
            .name("tag_2");

        var pet = new Pet()
            .name("doggie")
            .photoUrls(List.of (
                "https://example.com/picture_1.jpg",
                "https://example.com/picture_2.jpg"
            ))
            .id(12345L)
            .status(Pet.StatusEnum.AVAILABLE)
            .category(category)
            .tags(List.of (
                tags1,
                tags2
            ));

        try
        {
            var apiCaller = new PetApi(config);

            var response = apiCaller.addPet(
                pet
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Pet#addPet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
