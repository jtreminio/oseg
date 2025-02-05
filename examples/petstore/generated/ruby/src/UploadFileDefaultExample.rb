require "openapi_client"

OpenApiClient.configure do |config|
end

begin
    response = OpenApiClient::PetApi.new.upload_file(
        12345,
        {
            additional_metadata: "Additional data to pass to server",
            file: File.new("/path/to/file", "r"),
        },
    )

    p response
rescue OpenApiClient::ApiError => e
    puts "Exception when calling Pet#upload_file: #{e}"
end
