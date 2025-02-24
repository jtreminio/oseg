require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
    # config.api_key["api_key"] = "YOUR_API_KEY"
end

begin
    response = OpenApiClient::UserApi.new.get_user_by_name(
        "my_username", # username
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#get_user_by_name: #{e}"
end
