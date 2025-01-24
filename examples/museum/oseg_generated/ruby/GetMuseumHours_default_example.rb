require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

begin
    response = OpenApiMuseumClient::OperationsApi.new.get_museum_hours(
        {
            start_date: Date.parse("2023-02-23").to_date,
            page: 2,
            limit: 15,
        },
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Operations#get_museum_hours: #{e}"
end
