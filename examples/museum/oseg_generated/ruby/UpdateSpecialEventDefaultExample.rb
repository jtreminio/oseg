require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

special_event_fields = OpenApiMuseumClient::SpecialEventFields.new
special_event_fields.name = nil
special_event_fields.location = "On the beach."
special_event_fields.event_description = nil
special_event_fields.price = 15
special_event_fields.dates = nil

begin
    response = OpenApiMuseumClient::EventsApi.new.update_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
        special_event_fields,
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Events#update_special_event: #{e}"
end
