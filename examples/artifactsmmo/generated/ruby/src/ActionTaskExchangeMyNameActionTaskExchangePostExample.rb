require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_task_exchange_my_name_action_task_exchange_post(
        nil, // name
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_task_exchange_my_name_action_task_exchange_post: #{e}"
end
