require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::UserApi.new

    api_caller.delete_user(
        nil,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#delete_user: #{e}"
end
