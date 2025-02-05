require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    OpenApiClient::PetApi.new.update_pet_with_form(
        12345,
        {
            name: "Pet's new name",
            status: "sold",
        },
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#update_pet_with_form: #{e}"
end
