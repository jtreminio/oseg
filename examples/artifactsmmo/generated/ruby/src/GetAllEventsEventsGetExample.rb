require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::EventsApi.new.get_all_events_events_get(
        {
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Events#get_all_events_events_get: #{e}"
end
