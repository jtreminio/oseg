require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

special_event = OpenApiMuseumClient::SpecialEvent.new
special_event.name = "Mermaid Treasure Identification and Analysis"
special_event.location = "Under the seaaa 🦀 🎶 🌊."
special_event.event_description = "Join us as we review and classify a rare collection of 20 thingamabobs, gadgets, gizmos, whoosits, and whatsits, kindly donated by Ariel."
special_event.price = 0
special_event.dates = [
    Date.parse("2023-09-05").to_date,
    Date.parse("2023-09-08").to_date,
]
special_event.event_id = nil

begin
    response = OpenApiMuseumClient::EventsApi.new.create_special_event(
        special_event,
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Events#create_special_event: #{e}"
end
