require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
end

begin
    response = OpenApiClient::PetApi.new.find_pets_by_tags(
        [
            "tag_1",
            "tag_2",
        ], # tags
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#find_pets_by_tags: #{e}"
end
