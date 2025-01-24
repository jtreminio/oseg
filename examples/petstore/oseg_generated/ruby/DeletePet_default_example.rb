require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::PetApi.new.delete_pet(
        nil,
        {
            api_key: nil,
        },
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#delete_pet: #{e}"
end
