require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::ResourcesApi.new.get_all_resources_resources_get(
        {
            min_level: nil,
            max_level: nil,
            skill: nil,
            drop: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Resources#get_all_resources_resources_get: #{e}"
end
