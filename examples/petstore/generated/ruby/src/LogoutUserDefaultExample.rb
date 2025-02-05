require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    OpenApiClient::UserApi.new.logout_user
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#logout_user: #{e}"
end
