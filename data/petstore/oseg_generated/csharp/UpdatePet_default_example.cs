using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class UpdatePetDefaultExample
{
    public static void Main()
    {
        var config = new Configuration();

        var category = new Category(
            id: 12345,
            name: "Category_Name"
        );

        var tags1 = new Tag(
            id: 12345,
            name: "tag_1"
        );

        var tags2 = new Tag(
            id: 98765,
            name: "tag_2"
        );

        var pet = new Pet(
            name: "My pet name",
            photoUrls: new List<string>
            {
                "https://example.com/picture_1.jpg",
                "https://example.com/picture_1.jpg"
            },
            id: 12345,
            status: Pet.StatusEnum.Available,
            category: category,
            tags: new List<Tag>
            {
                tags1,
                tags2
            }
        );

        try
        {
            var apiCaller = new PetApi(config);

            var response = apiCaller.UpdatePet(
                pet: pet
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#UpdatePet: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
