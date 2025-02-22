require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.get_all_characters_logs_my_logs_get(
        {
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#get_all_characters_logs_my_logs_get: #{e}"
end
