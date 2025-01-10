require "openapimuseum_client"

OpenapiMuseumClient.configure do |config|
end

buy_museum_tickets = OpenapiMuseumClient::BuyMuseumTickets.new
buy_museum_tickets.ticket_type = "event"
buy_museum_tickets.event_id = "dad4bce8-f5cb-4078-a211-995864315e39"
buy_museum_tickets.ticket_date = "2023-09-05"
buy_museum_tickets.email = "todd@example.com"
buy_museum_tickets.ticket_id = nil

begin
    api_caller = OpenapiMuseumClient::TicketsApi.new

    response = api_caller.buy_museum_tickets(
        buy_museum_tickets,
    )

    p response
rescue OpenapiMuseumClient::ApiError => e
    puts "Exception when calling Tickets#buy_museum_tickets: #{e}"
end
