require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::PetApi.new.get_pet_by_id(
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#get_pet_by_id: #{e}"
end
