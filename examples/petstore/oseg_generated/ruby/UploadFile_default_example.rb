require "openapi_client"

OpenapiClient.configure do |config|
end

begin
    api_caller = OpenapiClient::PetApi.new

    response = api_caller.upload_file(
        12345,
        {
            additional_metadata: nil,
            file: File.new("/path/to/file", "r"),
        },
    )

    p response
rescue OpenapiClient::ApiError => e
    puts "Exception when calling Pet#upload_file: #{e}"
end
