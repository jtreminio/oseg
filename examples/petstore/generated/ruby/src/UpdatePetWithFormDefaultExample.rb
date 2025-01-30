require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::PetApi.new.update_pet_with_form(
        12345,
        {
            name: "Pet's new name",
            status: "sold",
        },
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#update_pet_with_form: #{e}"
end
