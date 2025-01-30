require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::UserApi.new.login_user(
        "my_username",
        "my_secret_password",
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#login_user: #{e}"
end
