require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::MapsApi.new.get_map_maps_x__y_get(
        nil, // x
        nil, // y
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Maps#get_map_maps_x__y_get: #{e}"
end
