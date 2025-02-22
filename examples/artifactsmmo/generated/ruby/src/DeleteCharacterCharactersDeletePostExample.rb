require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

delete_character_schema = ArtifactsMMOClient::DeleteCharacterSchema.new
delete_character_schema.name = nil

begin
    response = ArtifactsMMOClient::CharactersApi.new.delete_character_characters_delete_post(
        delete_character_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Characters#delete_character_characters_delete_post: #{e}"
end
