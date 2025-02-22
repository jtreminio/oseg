require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

deposit_withdraw_gold_schema = ArtifactsMMOClient::DepositWithdrawGoldSchema.new
deposit_withdraw_gold_schema.quantity = nil

begin
    response = ArtifactsMMOClient::MyCharactersApi.new.action_deposit_bank_gold_my_name_action_bank_deposit_gold_post(
        nil, // name
        deposit_withdraw_gold_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyCharacters#action_deposit_bank_gold_my_name_action_bank_deposit_gold_post: #{e}"
end
