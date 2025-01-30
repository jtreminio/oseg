require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::UserApi.new.logout_user
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#logout_user: #{e}"
end
