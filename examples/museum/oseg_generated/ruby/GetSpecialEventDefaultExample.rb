require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

begin
    response = OpenApiMuseumClient::EventsApi.new.get_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Events#get_special_event: #{e}"
end
