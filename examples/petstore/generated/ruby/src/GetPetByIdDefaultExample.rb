require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    response = OpenApiClient::PetApi.new.get_pet_by_id(
        12345,
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#get_pet_by_id: #{e}"
end
