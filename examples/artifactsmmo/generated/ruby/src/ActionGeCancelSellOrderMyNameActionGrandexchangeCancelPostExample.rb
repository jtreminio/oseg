require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

ge_cancel_order_schema = ArtifactsMMOClient::GECancelOrderSchema.new
ge_cancel_order_schema.id = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_ge_cancel_sell_order_my_name_action_grandexchange_cancel_post(
        nil, // name
        ge_cancel_order_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_ge_cancel_sell_order_my_name_action_grandexchange_cancel_post: #{e}"
end
