require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_buy_bank_expansion_my_name_action_bank_buy_expansion_post(
        nil, // name
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_buy_bank_expansion_my_name_action_bank_buy_expansion_post: #{e}"
end
