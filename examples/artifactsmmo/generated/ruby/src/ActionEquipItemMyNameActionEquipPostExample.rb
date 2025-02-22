require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

equip_schema = ArtifactsMMOClient::EquipSchema.new
equip_schema.code = nil
equip_schema.slot = nil
equip_schema.quantity = 1

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_equip_item_my_name_action_equip_post(
        nil, // name
        equip_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_equip_item_my_name_action_equip_post: #{e}"
end
