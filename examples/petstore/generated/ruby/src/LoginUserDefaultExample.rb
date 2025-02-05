require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    response = OpenApiClient::UserApi.new.login_user(
        "my_username",
        "my_secret_password",
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#login_user: #{e}"
end
