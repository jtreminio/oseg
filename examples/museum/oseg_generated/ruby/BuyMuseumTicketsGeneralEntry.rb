require "openapimuseum_client"

OpenApiMuseumClient.configure do |config|
end

buy_museum_tickets = OpenApiMuseumClient::BuyMuseumTickets.new
buy_museum_tickets.ticket_type = "general"
buy_museum_tickets.ticket_date = Date.parse("2023-09-07").to_date
buy_museum_tickets.email = "todd@example.com"
buy_museum_tickets.ticket_id = nil
buy_museum_tickets.event_id = nil

begin
    response = OpenApiMuseumClient::TicketsApi.new.buy_museum_tickets(
        buy_museum_tickets,
    )

    p response
rescue OpenApiMuseumClient::ApiError => e
    puts "Exception when calling Tickets#buy_museum_tickets: #{e}"
end
