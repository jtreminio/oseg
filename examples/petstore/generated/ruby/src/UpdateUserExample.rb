require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

user = OpenApiClient::User.new
user.id = 12345
user.username = "new-username"
user.first_name = "Joe"
user.last_name = "Broke"
user.email = "some-email@example.com"
user.password = "so secure omg"
user.phone = "555-867-5309"
user.user_status = 1

begin
    OpenApiClient::UserApi.new.update_user(
        "my-username", # username
        user,
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#update_user: #{e}"
end
