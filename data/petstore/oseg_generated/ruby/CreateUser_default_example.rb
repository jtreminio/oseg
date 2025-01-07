require "openapi_client"

OpenapiClient.configure do |config|
end

user = OpenapiClient::User.new
user.id = 12345
user.username = "my_user"
user.first_name = "John"
user.last_name = "Doe"
user.email = "john@example.com"
user.password = "secure_123"
user.phone = "555-123-1234"
user.user_status = 1

begin
    api_caller = OpenapiClient::UserApi.new

    api_caller.create_user(
        user,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#create_user: #{e}"
end
