require "openapi_client"

OpenapiClient.configure do |config|
end

user_1 = OpenapiClient::User.new
user_1.id = 12345
user_1.username = "my_user"
user_1.first_name = "John"
user_1.last_name = "Doe"
user_1.email = "john@example.com"
user_1.password = "secure_123"
user_1.phone = "555-123-1234"
user_1.user_status = 1

user_2 = OpenapiClient::User.new
user_2.id = 12345
user_2.username = "my_user"
user_2.first_name = "John"
user_2.last_name = "Doe"
user_2.email = "john@example.com"
user_2.password = "secure_123"
user_2.phone = "555-123-1234"
user_2.user_status = 1

user = [
    user_1,
    user_2,
]

begin
    api_caller = OpenapiClient::UserApi.new

    api_caller.create_users_with_list_input(
        user,
    )
rescue OpenapiClient::ApiError => e
    puts "Exception when calling User#create_users_with_list_input: #{e}"
end
