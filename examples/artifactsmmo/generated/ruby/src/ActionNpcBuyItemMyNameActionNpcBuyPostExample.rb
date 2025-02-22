require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

npc_merchant_buy_schema = ArtifactsMMOClient::NpcMerchantBuySchema.new
npc_merchant_buy_schema.code = nil
npc_merchant_buy_schema.quantity = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_npc_buy_item_my_name_action_npc_buy_post(
        nil, // name
        npc_merchant_buy_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_npc_buy_item_my_name_action_npc_buy_post: #{e}"
end
