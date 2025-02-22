require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::DefaultApi.new.get_status_get

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Default#get_status_get: #{e}"
end
