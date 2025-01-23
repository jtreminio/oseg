require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

begin
    api_caller = OpenapiMuseumClient::TicketsApi.new

    response = api_caller.get_ticket_code(
        "a54a57ca-36f8-421b-a6b4-2e8f26858a4c",
    )

    FileUtils.cp(response.path, "path/to/file.zip")
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Tickets#get_ticket_code: #{e}"
end
