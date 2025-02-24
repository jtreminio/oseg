require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
end

begin
    OpenApiClient::PetApi.new.update_pet_with_form(
        12345, # pet_id
        {
            name: "Pet's new name",
            status: "sold",
        },
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#update_pet_with_form: #{e}"
end
