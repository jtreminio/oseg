require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::StoreApi.new.delete_order(
        "12345",
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#delete_order: #{e}"
end
