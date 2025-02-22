require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyAccountApi.new.get_ge_sell_history_my_grandexchange_history_get(
        {
            id: nil,
            code: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyAccount#get_ge_sell_history_my_grandexchange_history_get: #{e}"
end
