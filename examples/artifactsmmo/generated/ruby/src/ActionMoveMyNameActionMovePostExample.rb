require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

destination_schema = ArtifactsMMOClient::DestinationSchema.new
destination_schema.x = nil
destination_schema.y = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_move_my_name_action_move_post(
        nil, // name
        destination_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_move_my_name_action_move_post: #{e}"
end
