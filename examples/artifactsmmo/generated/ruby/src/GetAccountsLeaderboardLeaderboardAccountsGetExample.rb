require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::LeaderboardApi.new.get_accounts_leaderboard_leaderboard_accounts_get(
        {
            sort: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Leaderboard#get_accounts_leaderboard_leaderboard_accounts_get: #{e}"
end
