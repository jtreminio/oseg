require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::ResourcesApi.new.get_resource_resources_code_get(
        "copper_rocks", // code
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Resources#get_resource_resources_code_get: #{e}"
end
