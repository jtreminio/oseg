require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

add_character_schema = ArtifactsMMOClient::AddCharacterSchema.new
add_character_schema.name = nil
add_character_schema.skin = nil

begin
    response = ArtifactsMMOClient::CharactersApi.new.create_character_characters_create_post(
        add_character_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Characters#create_character_characters_create_post: #{e}"
end
