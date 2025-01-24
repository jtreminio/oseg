require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::StoreApi.new.delete_order(
        nil,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#delete_order: #{e}"
end
