require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::GrandExchangeApi.new.get_ge_sell_orders_grandexchange_orders_get(
        {
            code: nil,
            seller: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling GrandExchange#get_ge_sell_orders_grandexchange_orders_get: #{e}"
end
