require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.get_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#get_special_event: #{e}"
end
