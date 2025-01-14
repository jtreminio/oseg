=begin
#Redocly Museum API

#Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.

The version of the OpenAPI document: 1.2.1
Contact: team@redocly.com
Generated by: https://openapi-generator.tech
Generator version: 7.8.0

=end

require 'cgi'

module OpenapiMuseumClient
  class OperationsApi
    attr_accessor :api_client

    def initialize(api_client = ApiClient.default)
      @api_client = api_client
    end
    # Get museum hours
    # Get upcoming museum operating hours.
    # @param [Hash] opts the optional parameters
    # @option opts [Date] :start_date Starting date to retrieve future operating hours from. Defaults to today&#39;s date.
    # @option opts [Integer] :page Page number to retrieve. (default to 1)
    # @option opts [Integer] :limit Number of days per page. (default to 10)
    # @return [Array<MuseumDailyHours>]
    def get_museum_hours(opts = {})
      data, _status_code, _headers = get_museum_hours_with_http_info(opts)
      data
    end

    # Get museum hours
    # Get upcoming museum operating hours.
    # @param [Hash] opts the optional parameters
    # @option opts [Date] :start_date Starting date to retrieve future operating hours from. Defaults to today&#39;s date.
    # @option opts [Integer] :page Page number to retrieve. (default to 1)
    # @option opts [Integer] :limit Number of days per page. (default to 10)
    # @return [Array<(Array<MuseumDailyHours>, Integer, Hash)>] Array<MuseumDailyHours> data, response status code and response headers
    def get_museum_hours_with_http_info(opts = {})
      if @api_client.config.debugging
        @api_client.config.logger.debug 'Calling API: OperationsApi.get_museum_hours ...'
      end
      if @api_client.config.client_side_validation && !opts[:'limit'].nil? && opts[:'limit'] > 30
        fail ArgumentError, 'invalid value for "opts[:"limit"]" when calling OperationsApi.get_museum_hours, must be smaller than or equal to 30.'
      end

      # resource path
      local_var_path = '/museum-hours'

      # query parameters
      query_params = opts[:query_params] || {}
      query_params[:'startDate'] = opts[:'start_date'] if !opts[:'start_date'].nil?
      query_params[:'page'] = opts[:'page'] if !opts[:'page'].nil?
      query_params[:'limit'] = opts[:'limit'] if !opts[:'limit'].nil?

      # header parameters
      header_params = opts[:header_params] || {}
      # HTTP header 'Accept' (if needed)
      header_params['Accept'] = @api_client.select_header_accept(['application/json', 'application/problem+json']) unless header_params['Accept']

      # form parameters
      form_params = opts[:form_params] || {}

      # http body (model)
      post_body = opts[:debug_body]

      # return_type
      return_type = opts[:debug_return_type] || 'Array<MuseumDailyHours>'

      # auth_names
      auth_names = opts[:debug_auth_names] || ['MuseumPlaceholderAuth']

      new_options = opts.merge(
        :operation => :"OperationsApi.get_museum_hours",
        :header_params => header_params,
        :query_params => query_params,
        :form_params => form_params,
        :body => post_body,
        :auth_names => auth_names,
        :return_type => return_type
      )

      data, status_code, headers = @api_client.call_api(:GET, local_var_path, new_options)
      if @api_client.config.debugging
        @api_client.config.logger.debug "API called: OperationsApi#get_museum_hours\nData: #{data.inspect}\nStatus code: #{status_code}\nHeaders: #{headers}"
      end
      return data, status_code, headers
    end
  end
end
