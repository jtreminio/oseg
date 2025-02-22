require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::AccountsApi.new.get_account_accounts_account_get(
        nil, // account
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Accounts#get_account_accounts_account_get: #{e}"
end
