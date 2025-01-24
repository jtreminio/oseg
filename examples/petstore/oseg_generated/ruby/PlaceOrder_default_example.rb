require "openapi_client"

OpenapiClient.configure do |config|
end

order = OpenapiClient::Order.new
order.id = 12345
order.pet_id = 98765
order.quantity = 5
order.ship_date = Date.parse("2025-01-01T17:32:28Z").to_time
order.status = "approved"
order.complete = false

begin
    response = OpenapiClient::StoreApi.new.place_order(
        order,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#place_order: #{e}"
end
