require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
    # config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    OpenApiClient::StoreApi.new.delete_order(
        "12345", # order_id
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Store#delete_order: #{e}"
end
