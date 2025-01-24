require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::PetApi.new.update_pet_with_form(
        nil,
        {
            name: nil,
            status: nil,
        },
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#update_pet_with_form: #{e}"
end
