require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::UserApi.new

    response = api_caller.get_user_by_name(
        nil,
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#get_user_by_name: #{e}"
end
