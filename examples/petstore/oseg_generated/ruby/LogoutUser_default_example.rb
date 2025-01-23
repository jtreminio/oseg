require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::UserApi.new

    api_caller.logout_user()
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#logout_user: #{e}"
end
