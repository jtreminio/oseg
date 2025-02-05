require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    OpenApiClient::UserApi.new.delete_user(
        "my_username",
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#delete_user: #{e}"
end
