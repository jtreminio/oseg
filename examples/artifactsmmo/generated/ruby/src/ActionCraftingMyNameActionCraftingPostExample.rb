require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

crafting_schema = ArtifactsMMOClient::CraftingSchema.new
crafting_schema.code = nil
crafting_schema.quantity = 1

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_crafting_my_name_action_crafting_post(
        nil, // name
        crafting_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_crafting_my_name_action_crafting_post: #{e}"
end
