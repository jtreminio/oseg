require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::PetApi.new.delete_pet(
        12345,
        {
            api_key: "df560d5ba4eb7adbc635c87c3931a8421ae24dc81646196cd66544fd4471414a",
        },
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#delete_pet: #{e}"
end
