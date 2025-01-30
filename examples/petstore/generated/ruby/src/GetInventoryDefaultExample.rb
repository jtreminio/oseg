require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::StoreApi.new.get_inventory

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#get_inventory: #{e}"
end
