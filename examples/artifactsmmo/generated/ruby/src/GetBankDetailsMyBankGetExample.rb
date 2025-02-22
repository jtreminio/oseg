require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

begin
    response = ArtifactsMMOClient::MyAccountApi.new.get_bank_details_my_bank_get

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyAccount#get_bank_details_my_bank_get: #{e}"
end
