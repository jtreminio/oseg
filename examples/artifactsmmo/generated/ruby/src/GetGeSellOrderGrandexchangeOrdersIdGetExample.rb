require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::GrandExchangeApi.new.get_ge_sell_order_grandexchange_orders_id_get(
        nil, // id
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling GrandExchange#get_ge_sell_order_grandexchange_orders_id_get: #{e}"
end
