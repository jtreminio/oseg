require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::PetApi.new

    api_caller.delete_pet(
        nil,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#delete_pet: #{e}"
end
