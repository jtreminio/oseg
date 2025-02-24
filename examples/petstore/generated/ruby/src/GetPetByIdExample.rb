require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    response = OpenApiClient::PetApi.new.get_pet_by_id(
        12345, # pet_id
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#get_pet_by_id: #{e}"
end
