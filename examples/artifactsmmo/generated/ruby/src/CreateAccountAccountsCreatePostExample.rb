require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

add_account_schema = ArtifactsMMOClient::AddAccountSchema.new
add_account_schema.username = nil
add_account_schema.password = nil
add_account_schema.email = nil

begin
    response = ArtifactsMMOClient::AccountsApi.new.create_account_accounts_create_post(
        add_account_schema,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Accounts#create_account_accounts_create_post: #{e}"
end
