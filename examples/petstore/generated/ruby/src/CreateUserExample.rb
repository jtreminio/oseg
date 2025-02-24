require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

user = OpenApiClient::User.new
user.id = 12345
user.username = "my_user"
user.first_name = "John"
user.last_name = "Doe"
user.email = "john@example.com"
user.password = "secure_123"
user.phone = "555-123-1234"
user.user_status = 1

begin
    OpenApiClient::UserApi.new.create_user(
        user,
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#create_user: #{e}"
end
