require "openapi_client"

OpenApiClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN"
end

begin
    response = OpenApiClient::PetApi.new.upload_file(
        12345, # pet_id
        {
            additional_metadata: "Additional data to pass to server",
            file: File.new("/path/to/file", "r"),
        },
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#upload_file: #{e}"
end
