require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    OpenapiClient::UserApi.new.delete_user(
        "my_username",
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#delete_user: #{e}"
end
