require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::PetApi.new

    api_caller.update_pet_with_form(
        nil,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#update_pet_with_form: #{e}"
end
