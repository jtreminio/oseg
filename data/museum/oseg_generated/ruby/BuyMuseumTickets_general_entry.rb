require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

buy_museum_tickets = OpenapiMuseumClient::BuyMuseumTickets.new

begin
    api_caller = OpenapiMuseumClient::TicketsApi.new

    response = api_caller.buy_museum_tickets(
        buy_museum_tickets,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Tickets#buy_museum_tickets: #{e}"
end
