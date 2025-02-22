require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::ItemsApi.new.get_all_items_items_get(
        {
            min_level: nil,
            max_level: nil,
            name: nil,
            type: nil,
            craft_skill: nil,
            craft_material: nil,
            page: 1,
            size: 50,
        },
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Items#get_all_items_items_get: #{e}"
end
