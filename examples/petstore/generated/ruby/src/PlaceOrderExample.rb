require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
    # config.api_key["api_key"] = "YOUR_API_KEY"
end

order = OpenApiClient::Order.new
order.id = 12345
order.pet_id = 98765
order.quantity = 5
order.ship_date = Date.parse("2025-01-01T17:32:28Z").to_time
order.status = "approved"
order.complete = false

begin
    response = OpenApiClient::StoreApi.new.place_order(
        order,
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Store#place_order: #{e}"
end
