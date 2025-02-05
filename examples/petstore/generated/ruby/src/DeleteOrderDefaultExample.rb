require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    OpenApiClient::StoreApi.new.delete_order(
        "12345",
    )
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Store#delete_order: #{e}"
end
