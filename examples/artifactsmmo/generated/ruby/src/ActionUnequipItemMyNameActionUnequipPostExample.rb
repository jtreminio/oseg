require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

unequip_schema = ArtifactsMMOClient::UnequipSchema.new
unequip_schema.slot = nil
unequip_schema.quantity = 1

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_unequip_item_my_name_action_unequip_post(
        nil, // name
        unequip_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_unequip_item_my_name_action_unequip_post: #{e}"
end
