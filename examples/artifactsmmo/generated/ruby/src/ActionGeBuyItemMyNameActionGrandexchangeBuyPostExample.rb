require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

ge_buy_order_schema = ArtifactsMMOClient::GEBuyOrderSchema.new
ge_buy_order_schema.id = nil
ge_buy_order_schema.quantity = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_ge_buy_item_my_name_action_grandexchange_buy_post(
        nil, // name
        ge_buy_order_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_ge_buy_item_my_name_action_grandexchange_buy_post: #{e}"
end
