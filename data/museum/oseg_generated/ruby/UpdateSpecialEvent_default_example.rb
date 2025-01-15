require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

special_event_fields = OpenapiMuseumClient::SpecialEventFields.new
special_event_fields.name = "Pirate Coding Workshop"
special_event_fields.location = "Computer Room"
special_event_fields.event_description = "Captain Blackbeard shares his love of the C...language. And possibly Arrrrr (R lang)."
special_event_fields.price = 25
special_event_fields.dates = nil

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.update_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
        special_event_fields,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#update_special_event: #{e}"
end
