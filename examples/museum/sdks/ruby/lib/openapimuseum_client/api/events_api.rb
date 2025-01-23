=begin
#Redocly Museum API

#Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.

The version of the OpenAPI document: 1.2.1
Contact: team@redocly.com
Generated by: https://openapi-generator.tech
Generator version: 7.11.0

=end

require 'cgi'

module OpenapiMuseumClient
  class EventsApi
    attr_accessor :api_client

    def initialize(api_client = ApiClient.default)
      @api_client = api_client
    end
    # New special event added
    # Publish details of a new or updated event.
    # @param [Hash] opts the optional parameters
    # @option opts [SpecialEvent] :special_event 
    # @return [nil]
    def publish_new_event(opts = {})
      publish_new_event_with_http_info(opts)
      nil
    end

    # New special event added
    # Publish details of a new or updated event.
    # @param [Hash] opts the optional parameters
    # @option opts [SpecialEvent] :special_event 
    # @return [Array<(nil, Integer, Hash)>] nil, response status code and response headers
    def publish_new_event_with_http_info(opts = {})
      if @api_client.config.debugging
        @api_client.config.logger.debug 'Calling API: EventsApi.publish_new_event ...'
      end
      # resource path
      local_var_path = '/publishNewEvent'

      # query parameters
      query_params = opts[:query_params] || {}

      # header parameters
      header_params = opts[:header_params] || {}
      # HTTP header 'Content-Type'
      content_type = @api_client.select_header_content_type(['application/json'])
      if !content_type.nil?
          header_params['Content-Type'] = content_type
      end

      # form parameters
      form_params = opts[:form_params] || {}

      # http body (model)
      post_body = opts[:debug_body] || @api_client.object_to_http_body(opts[:'special_event'])

      # return_type
      return_type = opts[:debug_return_type]

      # auth_names
      auth_names = opts[:debug_auth_names] || ['MuseumPlaceholderAuth']

      new_options = opts.merge(
        :operation => :"EventsApi.publish_new_event",
        :header_params => header_params,
        :query_params => query_params,
        :form_params => form_params,
        :body => post_body,
        :auth_names => auth_names,
        :return_type => return_type
      )

      data, status_code, headers = @api_client.call_api(:POST, local_var_path, new_options)
      if @api_client.config.debugging
        @api_client.config.logger.debug "API called: EventsApi#publish_new_event\nData: #{data.inspect}\nStatus code: #{status_code}\nHeaders: #{headers}"
      end
      return data, status_code, headers
    end
  end
end
