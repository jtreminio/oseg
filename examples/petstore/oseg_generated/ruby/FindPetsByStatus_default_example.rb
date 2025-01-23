require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::PetApi.new

    response = api_caller.find_pets_by_status(
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#find_pets_by_status: #{e}"
end
