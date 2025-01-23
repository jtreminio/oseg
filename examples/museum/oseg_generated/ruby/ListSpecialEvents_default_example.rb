require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

begin
    api_caller = OpenapiMuseumClient::EventsApi.new

    response = api_caller.list_special_events(
        {
            start_date: "2023-02-23",
            end_date: "2023-04-18",
            page: 2,
            limit: 15,
        },
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Events#list_special_events: #{e}"
end
