require "openapi_client"

OpenApiClient.configure do |config|
    config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    OpenApiClient::UserApi.new.logout_user
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#logout_user: #{e}"
end
