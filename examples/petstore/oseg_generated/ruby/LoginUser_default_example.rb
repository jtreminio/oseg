require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::UserApi.new.login_user(
        nil,
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#login_user: #{e}"
end
