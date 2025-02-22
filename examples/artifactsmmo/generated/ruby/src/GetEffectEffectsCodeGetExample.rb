require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::EffectsApi.new.get_effect_effects_code_get(
        nil, // code
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Effects#get_effect_effects_code_get: #{e}"
end
