require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

begin
    response = OpenApiMuseumClient::EventsApi.new.list_special_events(
        {
            start_date: Date.parse("2023-02-23").to_date,
            end_date: Date.parse("2023-04-18").to_date,
            page: 2,
            limit: 15,
        },
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Events#list_special_events: #{e}"
end
