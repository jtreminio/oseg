require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    response = OpenapiClient::PetApi.new.upload_file(
        12345,
        {
            additional_metadata: "Additional data to pass to server",
            file: File.new("/path/to/file", "r"),
        },
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#upload_file: #{e}"
end
