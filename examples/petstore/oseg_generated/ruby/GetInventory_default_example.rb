require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::StoreApi.new

    response = api_caller.get_inventory()

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#get_inventory: #{e}"
end
