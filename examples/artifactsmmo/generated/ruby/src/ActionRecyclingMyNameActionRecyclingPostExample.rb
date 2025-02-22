require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

recycling_schema = ArtifactsMMOClient::RecyclingSchema.new
recycling_schema.code = nil
recycling_schema.quantity = 1

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_recycling_my_name_action_recycling_post(
        nil, // name
        recycling_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_recycling_my_name_action_recycling_post: #{e}"
end
