=begin
#Redocly Museum API

#Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.

The version of the OpenAPI document: 1.2.1
Contact: team@redocly.com
Generated by: https://openapi-generator.tech
Generator version: 7.11.0

=end

# Common files
require 'openapimuseum_client/api_client'
require 'openapimuseum_client/api_error'
require 'openapimuseum_client/version'
require 'openapimuseum_client/configuration'

# Models
require 'openapimuseum_client/models/buy_museum_tickets'
require 'openapimuseum_client/models/error'
require 'openapimuseum_client/models/museum_daily_hours'
require 'openapimuseum_client/models/museum_tickets_confirmation'
require 'openapimuseum_client/models/special_event'
require 'openapimuseum_client/models/special_event_fields'
require 'openapimuseum_client/models/ticket'
require 'openapimuseum_client/models/ticket_type'

# APIs
require 'openapimuseum_client/api/events_api'
require 'openapimuseum_client/api/operations_api'
require 'openapimuseum_client/api/tickets_api'

module OpenApiMuseumClient
  class << self
    # Customize default settings for the SDK using block.
    #   OpenApiMuseumClient.configure do |config|
    #     config.username = "xxx"
    #     config.password = "xxx"
    #   end
    # If no block given, return the default Configuration object.
    def configure
      if block_given?
        yield(Configuration.default)
      else
        Configuration.default
      end
    end
  end
end
