require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

simple_item_schema = ArtifactsMMOClient::SimpleItemSchema.new
simple_item_schema.code = nil
simple_item_schema.quantity = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_deposit_bank_my_name_action_bank_deposit_post(
        nil, // name
        simple_item_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_deposit_bank_my_name_action_bank_deposit_post: #{e}"
end
