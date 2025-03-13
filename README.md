# OSEG - OpenAPI SDK Example Generator

Create (almost) ready to use SDK snippets for SDKs generated using [openapi-generator](https://openapi-generator.tech/) using example data from your OpenAPI spec.

## Examples

Several more examples can be found at [jtreminio/oseg-examples](https://github.com/jtreminio/oseg-examples).

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
using System.Text.Json;

using Org.OpenAPITools.Api;
using Org.OpenAPITools.Client;
using Org.OpenAPITools.Model;

namespace OSEG.PetStoreExamples;

public class AddPetExample
{
    public static void Run()
    {
        var config = new Configuration();
        config.AccessToken = "YOUR_ACCESS_TOKEN";

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

        var tags = new List<Tag>
        {
            tags1,
            tags2,
        };

        var pet = new Pet(
            name: "My pet name",
            photoUrls: [
                "https://example.com/picture_1.jpg",
                "https://example.com/picture_2.jpg",
            ],
            id: 12345,
            status: Pet.StatusEnum.Available,
            category: category,
            tags: tags
        );

        try
        {
            var response = new PetApi(config).AddPet(
                pet: pet
            );

            Console.WriteLine(response);
        }
        catch (ApiException e)
        {
            Console.WriteLine("Exception when calling PetApi#AddPet: " + e.Message);
            Console.WriteLine("Status Code: " + e.ErrorCode);
            Console.WriteLine(e.StackTrace);
        }
    }
}
```

### [java](https://openapi-generator.tech/docs/generators/java/)

```java
package oseg.petstore_examples;

import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.*;
import org.openapitools.client.auth.*;
import org.openapitools.client.JSON;
import org.openapitools.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class AddPetExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        ((HttpBearerAuth) config.getAuthentication("petstore_auth")).setBearerToken("YOUR_ACCESS_TOKEN");

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
            var response = new PetApi(config).addPet(
                pet
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling PetApi#addPet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### [kotlin](https://openapi-generator.tech/docs/generators/kotlin/)

```kotlin
package oseg.petstore_examples

import org.openapitools.client.infrastructure.*
import org.openapitools.client.apis.*
import org.openapitools.client.models.*

import java.io.File
import java.time.LocalDate
import java.time.OffsetDateTime
import kotlin.collections.ArrayList
import kotlin.collections.List
import kotlin.collections.Map
import com.squareup.moshi.adapter

@ExperimentalStdlibApi
class AddPetExample
{
    fun addPet()
    {
        ApiClient.accessToken = "YOUR_ACCESS_TOKEN"

        val category = Category(
            id = 12345,
            name = "Category_Name",
        )

        val tags1 = Tag(
            id = 12345,
            name = "tag_1",
        )

        val tags2 = Tag(
            id = 98765,
            name = "tag_2",
        )

        val tags = arrayListOf<Tag>(
            tags1,
            tags2,
        )

        val pet = Pet(
            name = "My pet name",
            photoUrls = listOf (
                "https://example.com/picture_1.jpg",
                "https://example.com/picture_2.jpg",
            ),
            id = 12345,
            status = Pet.Status.available,
            category = category,
            tags = tags,
        )

        try
        {
            val response = PetApi().addPet(
                pet = pet,
            )

            println(response)
        } catch (e: ClientException) {
            println("4xx response calling PetApi#addPet")
            e.printStackTrace()
        } catch (e: ServerException) {
            println("5xx response calling PetApi#addPet")
            e.printStackTrace()
        }
    }
}
```

### [php](https://openapi-generator.tech/docs/generators/php/)

```php
<?php

namespace OSEG\PetStoreExamples;

require_once __DIR__ . '/../vendor/autoload.php';

use SplFileObject;
use OpenAPI;

$config = OpenAPI\Client\Configuration::getDefaultConfiguration();
$config->setAccessToken("YOUR_ACCESS_TOKEN");

$category = (new OpenAPI\Client\Model\Category())
    ->setId(12345)
    ->setName("Category_Name");

$tags_1 = (new OpenAPI\Client\Model\Tag())
    ->setId(12345)
    ->setName("tag_1");

$tags_2 = (new OpenAPI\Client\Model\Tag())
    ->setId(98765)
    ->setName("tag_2");

$tags = [
    $tags_1,
    $tags_2,
];

$pet = (new OpenAPI\Client\Model\Pet())
    ->setName("My pet name")
    ->setPhotoUrls([
        "https://example.com/picture_1.jpg",
        "https://example.com/picture_2.jpg",
    ])
    ->setId(12345)
    ->setStatus(OpenAPI\Client\Model\Pet::STATUS_AVAILABLE)
    ->setCategory($category)
    ->setTags($tags);

try {
    $response = (new OpenAPI\Client\Api\PetApi(config: $config))->addPet(
        pet: $pet,
    );

    print_r($response);
} catch (OpenAPI\Client\ApiException $e) {
    echo "Exception when calling PetApi#addPet: {$e->getMessage()}";
}
```

### [python](https://openapi-generator.tech/docs/generators/python/)

```python
import json
from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    category = models.Category(
        id=12345,
        name="Category_Name",
    )

    tags_1 = models.Tag(
        id=12345,
        name="tag_1",
    )

    tags_2 = models.Tag(
        id=98765,
        name="tag_2",
    )

    tags = [
        tags_1,
        tags_2,
    ]

    pet = models.Pet(
        name="My pet name",
        photoUrls=[
            "https://example.com/picture_1.jpg",
            "https://example.com/picture_2.jpg",
        ],
        id=12345,
        status="available",
        category=category,
        tags=tags,
    )

    try:
        response = api.PetApi(api_client).add_pet(
            pet=pet,
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling PetApi#add_pet: %s\n" % e)
```

### [ruby](https://openapi-generator.tech/docs/generators/ruby/)

```ruby
require "json"
require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
end

category = OpenApiClient::Category.new
category.id = 12345
category.name = "Category_Name"

tags_1 = OpenApiClient::Tag.new
tags_1.id = 12345
tags_1.name = "tag_1"

tags_2 = OpenApiClient::Tag.new
tags_2.id = 98765
tags_2.name = "tag_2"

tags = [
    tags_1,
    tags_2,
]

pet = OpenApiClient::Pet.new
pet.name = "My pet name"
pet.photo_urls = [
    "https://example.com/picture_1.jpg",
    "https://example.com/picture_2.jpg",
]
pet.id = 12345
pet.status = "available"
pet.category = category
pet.tags = tags

begin
    response = OpenApiClient::PetApi.new.add_pet(
        pet,
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling PetApi#add_pet: #{e}"
end
```

### [typescript-node](https://openapi-generator.tech/docs/generators/typescript-node/)

```typescript
import * as fs from 'fs';
import api from "openapi_client"
import models from "openapi_client"

const apiCaller = new api.PetApi();
apiCaller.accessToken = "YOUR_ACCESS_TOKEN";

const category = new models.Category();
category.id = 12345;
category.name = "Category_Name";

const tags1 = new models.Tag();
tags1.id = 12345;
tags1.name = "tag_1";

const tags2 = new models.Tag();
tags2.id = 98765;
tags2.name = "tag_2";

const tags = [
  tags1,
  tags2,
];

const pet = new models.Pet();
pet.name = "My pet name";
pet.photoUrls = [
  "https://example.com/picture_1.jpg",
  "https://example.com/picture_2.jpg",
];
pet.id = 12345;
pet.status = models.Pet.StatusEnum.Available;
pet.category = category;
pet.tags = tags;

apiCaller.addPet(
  pet,
).then(response => {
  console.log(response.body);
}).catch(error => {
  console.log("Exception when calling PetApi#addPet:");
  console.log(error.body);
});
```

## Where does the example data come from?

Example data used to generate the code snippets can come from a number of places:

* [example or examples values](https://github.com/jtreminio/oseg-examples/blob/main/petstore/openapi.yaml#L705) in schema
* [default values](https://github.com/jtreminio/oseg-examples/blob/main/petstore/openapi.yaml#L100) in schema
* [Externally referenced JSON files](https://github.com/jtreminio/oseg/blob/51e26de23b812f22887d0ccc867b09dff825fbf9/tests/fixtures/example_data_parser-external_example.yaml#L78-L82) defined in schema
* You can also create a [JSON file with examples for all the endpoints you want](https://github.com/jtreminio/oseg-examples/blob/main/petstore/example_data.json)

OSEG currently generates one code snippet file per `requestBody` definition, but only a single example per `parameters` definition.

In other words, you can generate multiple examples of the same operation/endpoint by having multiple `requestBody` definitions. Each generate example will have different data embedded within it. However, since [parameters](https://github.com/jtreminio/oseg-examples/blob/main/petstore/openapi.yaml#L84-L100) is tied to a single operation, the same data will apply to any and all `requestBody` definitions.

If you use a custom JSON file with examples you can define as many examples per endpoint as you want, since you can define each data source separately (`query`, `path`, `header`, `cookie`, and `body`) per endpoint.

## Adding more SDKs

Examples are generated using (fairly) simple [Jinja templates](https://github.com/jtreminio/oseg/tree/main/oseg/templates). Adding a new SDK requires a few steps:

1) Create the Generator
   * handles language-specific parameter and method naming
   * contains a config class with required and optional parameters for the chosen SDK. We follow the naming convention outlined in [openapi-generator page for each generator](https://openapi-generator.tech/docs/generators/python).
   * and some other things
   * [Python example](https://github.com/jtreminio/oseg/blob/main/oseg/generator/python_generator.py)
2) Create the Jinja template ([Python example](https://github.com/jtreminio/oseg/blob/main/oseg/generator/python_generator.py))

## How to run

The entrypoint to this project is [run.py](https://github.com/jtreminio/oseg/blob/main/run.py). It currently supports two commands:

### config-help

Prints all config options available to a given generator.

Run `python3 run.py config-help --help` for more details.

Or, with Docker: `docker container run --rm jtreminio/oseg:latest config-help --help`

Show config options for the `python` generator:

```bash
python3 run.py config-help -g python
```

Or, with Docker: 

```bash
docker container run --rm jtreminio/oseg:latest config-help -g python
```

### generate

Generates the SDK snippets and writes to specified location.

Run `python3 run.py generate --help` for more details.

Run with a local config file:

```bash
python3 run.py generate \
    -i openapi.yaml \
    -o python/src \
    --config-file config-python.yaml \
    --example-data-file example_data.json
```

Or, with Docker:

```bash
docker container run --rm -v $PWD:/app jtreminio/oseg:latest generate \
    -i openapi.yaml \
    -o python/src \
    --config-file config-python.yaml \
    --example-data-file example_data.json
```

Run with inline config values. These config values can be seen by running `python3 run.py config-help -g {generator}`:

```bash
python3 run.py generate \
    -i openapi.yaml \
    -o python/src \
    --generator-name python \
    --config '{
      "packageName": "openapi_client",
      "oseg.propertyNamingConvention": "camel_case",
      "oseg.security.api_key.api_key": "YOUR_API_KEY",
      "oseg.security.petstore_auth.access_token": "YOUR_ACCESS_TOKEN"
    }' \
    --example-data-file example_data.json
```

Or, with Docker:

```bash
docker container run --rm -v $PWD:/app jtreminio/oseg:latest generate \
    -i openapi.yaml \
    -o python/src \
    --generator-name python \
    --config '{
      "packageName": "openapi_client",
      "oseg.propertyNamingConvention": "camel_case",
      "oseg.security.api_key.api_key": "YOUR_API_KEY",
      "oseg.security.petstore_auth.access_token": "YOUR_ACCESS_TOKEN"
    }' \
    --example-data-file example_data.json
```

## Tests

See [tests directory](https://github.com/jtreminio/oseg/tree/main/tests).

## Feature support

The aim of this project is to cover the most common use-cases in an OpenAPI spec. 

### Supported 

* Requests with and without formdata: `openapi-generator` will create a different interface if an endpoint's `content-type` has formdata (`multipart/form-data` or `application/x-www-form-urlencoded`) and everything else
* Discriminators with `allOf`

### Issues

The following are issues with the SDK code generated by `openapi-generator`.

* `allOf` without a discriminator: Depending on the `openapi-generator` generator used, the generated SDK may be completely broken
  * `typescript-node` SDK code is generated broken by `openapi-generator` 
  * Other SDKs currently supported by OSEG will usually just use a generic `object` type
* `anyOf`
  * `typescript-node` generated SDK does not set data
  * `php` generated SDK does not set data
  * Other SDKs currently supported by OSEG generate a class
* `oneOf`
  * `typescript-node` generated SDK does not set data
  * `php` generated SDK does not set data
  * Other SDKs currently supported by OSEG generate a class
* Multiple values in `type` definition. New in OpenAPI 3.1 `type` can now be an array of supported types
  * `c#`, `java`, `ruby` Generate a class
  * `python` generates a class but does not use it, types property as the first value in `type`
  * `php` generates a class, data not set
  * `typescript-node` generates a class, data not set
* `openapi-generator` generates a class for inline schema with `type=object`. If two or more Operations share identical inline schema definitions, `openapi-generator` will only generate a class for one of the Operations, and all Operations will reference this class. The name of the class depends on which Operation is read first by `openapi-generator`, but it may not reflect the first definition within the OAS file and thus is impossible for OSEG to know the name of the class ahead of time.
