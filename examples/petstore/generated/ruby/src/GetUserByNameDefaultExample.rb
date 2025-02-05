require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    response = OpenApiClient::UserApi.new.get_user_by_name(
        "my_username",
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling User#get_user_by_name: #{e}"
end
