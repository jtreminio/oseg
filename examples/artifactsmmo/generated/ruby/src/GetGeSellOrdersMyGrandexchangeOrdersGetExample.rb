require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyAccountApi.new.get_ge_sell_orders_my_grandexchange_orders_get(
        {
            code: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyAccount#get_ge_sell_orders_my_grandexchange_orders_get: #{e}"
end
