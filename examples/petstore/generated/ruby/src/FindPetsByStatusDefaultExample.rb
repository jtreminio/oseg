require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::PetApi.new.find_pets_by_status(
        [
            "available",
            "pending",
        ],
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#find_pets_by_status: #{e}"
end
