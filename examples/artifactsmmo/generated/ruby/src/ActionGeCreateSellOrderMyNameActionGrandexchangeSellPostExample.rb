require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

ge_order_creationr_schema = ArtifactsMMOClient::GEOrderCreationrSchema.new
ge_order_creationr_schema.code = nil
ge_order_creationr_schema.quantity = nil
ge_order_creationr_schema.price = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_ge_create_sell_order_my_name_action_grandexchange_sell_post(
        nil, // name
        ge_order_creationr_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_ge_create_sell_order_my_name_action_grandexchange_sell_post: #{e}"
end
