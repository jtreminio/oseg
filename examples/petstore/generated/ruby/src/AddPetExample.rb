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
    puts "Exception when calling Pet#add_pet: #{e}"
end
