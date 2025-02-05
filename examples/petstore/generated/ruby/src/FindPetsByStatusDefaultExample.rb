require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    response = OpenApiClient::PetApi.new.find_pets_by_status(
        [
            "available",
            "pending",
        ],
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#find_pets_by_status: #{e}"
end
