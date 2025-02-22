require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::BadgesApi.new.get_badge_badges_code_get(
        nil, // code
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Badges#get_badge_badges_code_get: #{e}"
end
