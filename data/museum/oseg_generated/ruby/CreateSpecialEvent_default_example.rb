require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

special_event = OpenapiMuseumClient::SpecialEvent.new

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.create_special_event(
        special_event,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#create_special_event: #{e}"
end
