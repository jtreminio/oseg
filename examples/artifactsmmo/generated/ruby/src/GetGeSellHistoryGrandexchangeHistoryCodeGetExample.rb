require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::GrandExchangeApi.new.get_ge_sell_history_grandexchange_history_code_get(
        nil, // code
        {
            seller: nil,
            buyer: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling GrandExchange#get_ge_sell_history_grandexchange_history_code_get: #{e}"
end
