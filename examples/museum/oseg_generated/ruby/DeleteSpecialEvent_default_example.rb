require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    api_caller.delete_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
    )
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#delete_special_event: #{e}"
end
