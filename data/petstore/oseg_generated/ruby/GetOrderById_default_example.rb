require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::StoreApi.new

    response = api_caller.get_order_by_id(
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#get_order_by_id: #{e}"
end
