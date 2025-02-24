require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
end

begin
    OpenApiClient::PetApi.new.delete_pet(
        12345, # pet_id
        {
            api_key: "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a",
        },
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#delete_pet: #{e}"
end
