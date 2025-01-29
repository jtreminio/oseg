require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

begin
    response = OpenApiMuseumClient::TicketsApi.new.get_ticket_code(
        "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
    )

    FileUtils.cp(response.path, "path/to/file.zip")
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Tickets#get_ticket_code: #{e}"
end
