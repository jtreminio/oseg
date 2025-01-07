# OSEG

**O**penAPI **S**DK **E**xample **G**enerator

Create (almost) ready to use SDK snippets for SDKs generated using [openapi-generator](https://openapi-generator.tech/) using example data from your OpenAPI spec.

## Examples

Using the [OpenAPITools/openapi-generator petstore.yaml](https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml) definition, we can generate SDK examples from the [addPet endpoint](https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/test/resources/2_0/petstore.yaml#L22-L47).

OpenAPI spec:

```yaml
    post:
      tags:
        - pet
      summary: Add a new pet to the store
      description: ''
      operationId: addPet
      consumes:
        - application/json
        - application/xml
      produces:
        - application/xml
        - application/json
      parameters:
        - in: body
          name: body
          description: Pet object that needs to be added to the store
          required: true
          schema:
            $ref: '#/definitions/Pet'
      responses:
        '405':
          description: Invalid input
      security:
        - petstore_auth:
            - 'write:pets'
            - 'read:pets'
```

Generated SDK examples:

### [csharp](https://openapi-generator.tech/docs/generators/csharp/)

```csharp
using System;
using System.Collections.Generic;
using System.IO;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

public class AddPetDefaultExample
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
            name: "doggie",
            photoUrls: new List<string>
            {
                "https://example.com/picture_1.jpg",
                "https://example.com/picture_2.jpg"
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

            var response = apiCaller.AddPet(
                pet: pet
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling Pet#AddPet: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
```

### [java](https://openapi-generator.tech/docs/generators/java/)

```java
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
```

### [php](https://openapi-generator.tech/docs/generators/php/)

```php
<?php

require_once __DIR__ . '/vendor/autoload.php';

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();

$category = (new OpenAPI\Client\Model\Category())
    ->setId(12345)
    ->setName("Category_Name");

$tags_1 = (new OpenAPI\Client\Model\Tag())
    ->setId(12345)
    ->setName("tag_1");

$tags_2 = (new OpenAPI\Client\Model\Tag())
    ->setId(98765)
    ->setName("tag_2");

$pet = (new OpenAPI\Client\Model\Pet())
    ->setName("doggie")
    ->setPhotoUrls([
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_2.jpg",
    ])
    ->setId(12345)
    ->setStatus(OpenAPI\Client\Model\Pet::STATUS_AVAILABLE)
    ->setCategory($category)
    ->setTags([
        $tags_1,
        $tags_2,
    ]);

try {
    $api_caller = new OpenAPI\Client\Api\PetApi(config: $config);

    $response = $api_caller->addPet(
        pet: $pet,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo 'Exception when calling Pet#addPet: '
        . print_r($e->getResponseObject());
}
```

### [python](https://openapi-generator.tech/docs/generators/python/)

```python
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    category = models.Category()
    category.id = 12345
    category.name = "Category_Name"

    tags_1 = models.Tag()
    tags_1.id = 12345
    tags_1.name = "tag_1"

    tags_2 = models.Tag()
    tags_2.id = 98765
    tags_2.name = "tag_2"

    pet = models.Pet()
    pet.name = "doggie"
    pet.photoUrls = [
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_2.jpg",
    ]
    pet.id = 12345
    pet.status = "available"
    pet.category = category
    pet.tags = [
        tags_1,
        tags_2,
    ]

    try:
        api_caller = api.PetApi(api_client)

        response = api_caller.add_pet(
            pet=pet,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#add_pet: %s\n" % e)
```

### [ruby](https://openapi-generator.tech/docs/generators/ruby/)

```ruby
require "openapi_client"

OpenapiClient.configure do |config|
end

category = OpenapiClient::Category.new
category.id = 12345
category.name = "Category_Name"

tags_1 = OpenapiClient::Tag.new
tags_1.id = 12345
tags_1.name = "tag_1"

tags_2 = OpenapiClient::Tag.new
tags_2.id = 98765
tags_2.name = "tag_2"

pet = OpenapiClient::Pet.new
pet.name = "doggie"
pet.photo_urls = [
    "https://example.com/picture_1.jpg",
    "https://example.com/picture_2.jpg",
]
pet.id = 12345
pet.status = "available"
pet.category = category
pet.tags = [
    tags_1,
    tags_2,
]

begin
    api_caller = OpenapiClient::PetApi.new

    response = api_caller.add_pet(
        pet,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#add_pet: #{e}"
end
```

### [typescript-node](https://openapi-generator.tech/docs/generators/typescript-node/)

```typescript
import * as fs from 'fs';
import * as openapi_client from "openapi_client";

const apiCaller = new openapi_client.PetApi();

const category: openapi_client.Category = {
    id: 12345,
    name: "Category_Name",
};

const tags_1: openapi_client.Tag = {
    id: 12345,
    name: "tag_1",
};

const tags_2: openapi_client.Tag = {
    id: 98765,
    name: "tag_2",
};

const pet: openapi_client.Pet = {
    name: "doggie",
    photoUrls: [
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_2.jpg",
    ],
    id: 12345,
    status: openapi_client.Pet.StatusEnum.Available,
    category: category,
    tags: [
        tags_1,
        tags_2,
    ],
};

apiCaller.addPet(
    pet,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling Pet#addPet:");
  console.log(error.body);
});
```

## Where does the example data come from?

Example data embedded into the snippets above is read from a number of places, almost all embedded within the OpenAPI definition itself:

1) `example` or `examples` definition among operation or parameter definitions
2) Externally referenced JSON files
3) You can also create custom JSON payloads for any given endpoint. Right now the directory for this is hard-coded as `custom_examples` within your OpenAPI SDK config file's directory. See [custom_examples](./data/petstore/custom_examples)

OSEG currently generates one example file per `requestBody` definition, but only a single example per `parameters` definition.

In other words, you can generate multiple examples of the same operation/endpoint by having multiple `requestBody` definitions (`application/json` and `application/x-www-form-urlencoded`). Each generate example will have different data embedded within it. However, since [parameters](https://github.com/jtreminio/oseg/blob/main/data/petstore/openapi.yaml#L84-L100) is tied to a single operation, the same data will apply to any and all `requestBody` definitions.

## Adding more SDKs

Examples are generated using (fairly) simple [Jinja templates](./oseg/templates/). Adding a new SDK requires a few steps:

1) Create the OpenAPI config file ([Python example](./data/petstore/config-python.yaml))
2) Create the Jinja extension class that handles language-specific parameter and method naming, and some other things ([Python example](./oseg/jinja_extension/python_extension.py))
3) Create the Jinja template ([Python example](./oseg/templates/python.jinja2))

## How to run

This project is in its infancy, for now to run it you simply run [run.py](./run.py)

Generated examples are output in [./data/petstore/oseg_generated/{sdk}](./data/petstore/oseg_generated).

## Tests

Tests are being written!

## Feature support

The aim of this project is to cover the most common use-cases in an OpenAPI spec. 

Things like discriminators and `allOf` will be supported.

Things like `oneOf` will not be supported (this does not translate very well to generated SDKs).

Currently only languages I know are supported. I will continue adding more language as the project matures and test coverage increases.

OSEG does not currently embed authentication/security examples or anything unrelated to data not available from `example`/`examples`. More feature support is coming.
