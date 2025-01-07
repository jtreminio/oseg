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
