require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::AccountsApi.new.get_account_achievements_accounts_account_achievements_get(
        nil, // account
        {
            type: nil,
            completed: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Accounts#get_account_achievements_accounts_account_achievements_get: #{e}"
end
