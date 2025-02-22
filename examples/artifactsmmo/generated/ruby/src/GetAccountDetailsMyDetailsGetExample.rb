require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyAccountApi.new.get_account_details_my_details_get

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyAccount#get_account_details_my_details_get: #{e}"
end
