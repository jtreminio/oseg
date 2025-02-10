require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.api_key = "YOUR_API_KEY";
end

begin
    response = OpenApiClient::StoreApi.new.get_order_by_id(
        3,
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Store#get_order_by_id: #{e}"
end
