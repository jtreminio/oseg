require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.username = "YOUR_USERNAME";
    config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::TokenApi.new.generate_token_token_post

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Token#generate_token_token_post: #{e}"
end
