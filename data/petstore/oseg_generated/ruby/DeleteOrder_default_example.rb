require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::StoreApi.new

    api_caller.delete_order(
        nil,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#delete_order: #{e}"
end
