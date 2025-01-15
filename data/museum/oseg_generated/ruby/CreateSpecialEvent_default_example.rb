require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

special_event = OpenapiMuseumClient::SpecialEvent.new
special_event.name = "Pirate Coding Workshop"
special_event.location = "Computer Room"
special_event.event_description = "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang)."
special_event.price = 25
special_event.dates = [
    "2023-09-05",
    "2023-09-08",
]
special_event.event_id = "3be6453c-03eb-4357-ae5a-984a0e574a54"

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.create_special_event(
        special_event,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#create_special_event: #{e}"
end
