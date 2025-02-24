require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    response = OpenApiClient::StoreApi.new.get_inventory

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Store#get_inventory: #{e}"
end
