require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::CharactersApi.new.get_character_characters_name_get(
        nil, // name
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Characters#get_character_characters_name_get: #{e}"
end
