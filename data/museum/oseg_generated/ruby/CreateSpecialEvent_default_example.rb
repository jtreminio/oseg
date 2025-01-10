require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

special_event = OpenapiMuseumClient::SpecialEvent.new
special_event.name = "Mermaid Treasure Identification and Analysis"
special_event.location = "Under the seaaa 🦀 🎶 🌊."
special_event.event_description = "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel."
special_event.price = 0
special_event.event_id = nil

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.create_special_event(
        special_event,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#create_special_event: #{e}"
end
