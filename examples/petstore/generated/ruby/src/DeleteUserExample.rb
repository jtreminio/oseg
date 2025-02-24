require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    OpenApiClient::UserApi.new.delete_user(
        "my_username", # username
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#delete_user: #{e}"
end
