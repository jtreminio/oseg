require "openapi_client"

OpenapiClient.configure do |config|
end

user = OpenapiClient::User.new
user.id = 12345
user.username = "new-username"
user.first_name = "Joe"
user.last_name = "Broke"
user.email = "some-email@example.com"
user.password = "so secure omg"
user.phone = "555-867-5309"
user.user_status = 1

begin
    OpenapiClient::UserApi.new.update_user(
        "my-username",
        user,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#update_user: #{e}"
end
