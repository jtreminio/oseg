require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

begin
    OpenApiMuseumClient::EventsApi.new.delete_special_event(
        "dad4bce8-f5cb-4078-a211-995864315e39",
    )
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Events#delete_special_event: #{e}"
end
