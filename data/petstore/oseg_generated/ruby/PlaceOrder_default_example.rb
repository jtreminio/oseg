require "openapi_client"

OpenapiClient.configure do |config|
end

order = OpenapiClient::Order.new
order.id = 12345
order.pet_id = 98765
order.quantity = 5
order.ship_date = "2025-01-01T17:32:28Z"
order.status = "approved"
order.complete = false

begin
    api_caller = OpenapiClient::StoreApi.new

    response = api_caller.place_order(
        order,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Store#place_order: #{e}"
end
