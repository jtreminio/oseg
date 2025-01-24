require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::PetApi.new.find_pets_by_tags(
        [
            "tag_1",
            "tag_2",
        ],
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#find_pets_by_tags: #{e}"
end
