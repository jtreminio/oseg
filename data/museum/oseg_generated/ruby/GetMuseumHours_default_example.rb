require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

begin
    api_caller = OpenapiMuseumClient::OperationsApi.new

    response = api_caller.get_museum_hours(
        {
            start_date: "2023-02-23",
            page: 2,
            limit: 15,
        },
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Operations#get_museum_hours: #{e}"
end
