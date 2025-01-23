require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::PetApi.new

    response = api_caller.get_pet_by_id(
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#get_pet_by_id: #{e}"
end
