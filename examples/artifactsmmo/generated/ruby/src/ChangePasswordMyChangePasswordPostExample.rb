require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
end

change_password = ArtifactsMMOClient::ChangePassword.new
change_password.current_password = nil
change_password.new_password = nil

begin
    response = ArtifactsMMOClient::MyAccountApi.new.change_password_my_change_password_post(
        change_password,
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling MyAccount#change_password_my_change_password_post: #{e}"
end
