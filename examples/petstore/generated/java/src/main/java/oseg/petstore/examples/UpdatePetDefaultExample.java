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

public class UpdatePetDefaultExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setAccessToken("YOUR_ACCESS_TOKEN");

        var category = new Category();
        category.id(12345L);
        category.name("Category_Name");

        var tags1 = new Tag();
        tags1.id(12345L);
        tags1.name("tag_1");

        var tags2 = new Tag();
        tags2.id(98765L);
        tags2.name("tag_2");

        var tags = new ArrayList<Tag>(List.of (
            tags1,
            tags2
        ));

        var pet = new Pet();
        pet.name("My pet name");
        pet.photoUrls(List.of (
            "https://example.com/picture_1.jpg",
            "https://example.com/picture_2.jpg"
        ));
        pet.id(12345L);
        pet.status(Pet.StatusEnum.AVAILABLE);
        pet.category(category);
        pet.tags(tags);

        try
        {
            var response = new PetApi(config).updatePet(
                pet
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Pet#updatePet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
