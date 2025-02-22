require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.get_my_characters_my_characters_get

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#get_my_characters_my_characters_get: #{e}"
end
