/*
 * Redocly Museum API
 *
 * Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.
 *
 * The version of the OpenAPI document: 1.2.1
 * Contact: team@redocly.com
 * Generated by: https://github.com/openapitools/openapi-generator.git
 */


using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Net;
using System.Net.Mime;
using Org.OpenAPIMuseum.Client;
using Org.OpenAPIMuseum.Model;

namespace Org.OpenAPIMuseum.Api
{

    /// <summary>
    /// Represents a collection of functions to interact with the API endpoints
    /// </summary>
    public interface ITicketsApiSync : IApiAccessor
    {
        #region Synchronous Operations
        /// <summary>
        /// Buy museum tickets
        /// </summary>
        /// <remarks>
        /// Purchase museum tickets for general entry or special events.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>MuseumTicketsConfirmation</returns>
        MuseumTicketsConfirmation BuyMuseumTickets(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0);

        /// <summary>
        /// Buy museum tickets
        /// </summary>
        /// <remarks>
        /// Purchase museum tickets for general entry or special events.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>ApiResponse of MuseumTicketsConfirmation</returns>
        ApiResponse<MuseumTicketsConfirmation> BuyMuseumTicketsWithHttpInfo(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0);
        /// <summary>
        /// Get ticket QR code
        /// </summary>
        /// <remarks>
        /// Return an image of your ticket with scannable QR code. Used for event entry.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>System.IO.Stream</returns>
        System.IO.Stream GetTicketCode(Guid ticketId, int operationIndex = 0);

        /// <summary>
        /// Get ticket QR code
        /// </summary>
        /// <remarks>
        /// Return an image of your ticket with scannable QR code. Used for event entry.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>ApiResponse of System.IO.Stream</returns>
        ApiResponse<System.IO.Stream> GetTicketCodeWithHttpInfo(Guid ticketId, int operationIndex = 0);
        #endregion Synchronous Operations
    }

    /// <summary>
    /// Represents a collection of functions to interact with the API endpoints
    /// </summary>
    public interface ITicketsApiAsync : IApiAccessor
    {
        #region Asynchronous Operations
        /// <summary>
        /// Buy museum tickets
        /// </summary>
        /// <remarks>
        /// Purchase museum tickets for general entry or special events.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of MuseumTicketsConfirmation</returns>
        System.Threading.Tasks.Task<MuseumTicketsConfirmation> BuyMuseumTicketsAsync(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken));

        /// <summary>
        /// Buy museum tickets
        /// </summary>
        /// <remarks>
        /// Purchase museum tickets for general entry or special events.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of ApiResponse (MuseumTicketsConfirmation)</returns>
        System.Threading.Tasks.Task<ApiResponse<MuseumTicketsConfirmation>> BuyMuseumTicketsWithHttpInfoAsync(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken));
        /// <summary>
        /// Get ticket QR code
        /// </summary>
        /// <remarks>
        /// Return an image of your ticket with scannable QR code. Used for event entry.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of System.IO.Stream</returns>
        System.Threading.Tasks.Task<System.IO.Stream> GetTicketCodeAsync(Guid ticketId, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken));

        /// <summary>
        /// Get ticket QR code
        /// </summary>
        /// <remarks>
        /// Return an image of your ticket with scannable QR code. Used for event entry.
        /// </remarks>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of ApiResponse (System.IO.Stream)</returns>
        System.Threading.Tasks.Task<ApiResponse<System.IO.Stream>> GetTicketCodeWithHttpInfoAsync(Guid ticketId, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken));
        #endregion Asynchronous Operations
    }

    /// <summary>
    /// Represents a collection of functions to interact with the API endpoints
    /// </summary>
    public interface ITicketsApi : ITicketsApiSync, ITicketsApiAsync
    {

    }

    /// <summary>
    /// Represents a collection of functions to interact with the API endpoints
    /// </summary>
    public partial class TicketsApi : ITicketsApi
    {
        private Org.OpenAPIMuseum.Client.ExceptionFactory _exceptionFactory = (name, response) => null;

        /// <summary>
        /// Initializes a new instance of the <see cref="TicketsApi"/> class.
        /// </summary>
        /// <returns></returns>
        public TicketsApi() : this((string)null)
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="TicketsApi"/> class.
        /// </summary>
        /// <returns></returns>
        public TicketsApi(string basePath)
        {
            this.Configuration = Org.OpenAPIMuseum.Client.Configuration.MergeConfigurations(
                Org.OpenAPIMuseum.Client.GlobalConfiguration.Instance,
                new Org.OpenAPIMuseum.Client.Configuration { BasePath = basePath }
            );
            this.Client = new Org.OpenAPIMuseum.Client.ApiClient(this.Configuration.BasePath);
            this.AsynchronousClient = new Org.OpenAPIMuseum.Client.ApiClient(this.Configuration.BasePath);
            this.ExceptionFactory = Org.OpenAPIMuseum.Client.Configuration.DefaultExceptionFactory;
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="TicketsApi"/> class
        /// using Configuration object
        /// </summary>
        /// <param name="configuration">An instance of Configuration</param>
        /// <returns></returns>
        public TicketsApi(Org.OpenAPIMuseum.Client.Configuration configuration)
        {
            if (configuration == null) throw new ArgumentNullException("configuration");

            this.Configuration = Org.OpenAPIMuseum.Client.Configuration.MergeConfigurations(
                Org.OpenAPIMuseum.Client.GlobalConfiguration.Instance,
                configuration
            );
            this.Client = new Org.OpenAPIMuseum.Client.ApiClient(this.Configuration.BasePath);
            this.AsynchronousClient = new Org.OpenAPIMuseum.Client.ApiClient(this.Configuration.BasePath);
            ExceptionFactory = Org.OpenAPIMuseum.Client.Configuration.DefaultExceptionFactory;
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="TicketsApi"/> class
        /// using a Configuration object and client instance.
        /// </summary>
        /// <param name="client">The client interface for synchronous API access.</param>
        /// <param name="asyncClient">The client interface for asynchronous API access.</param>
        /// <param name="configuration">The configuration object.</param>
        public TicketsApi(Org.OpenAPIMuseum.Client.ISynchronousClient client, Org.OpenAPIMuseum.Client.IAsynchronousClient asyncClient, Org.OpenAPIMuseum.Client.IReadableConfiguration configuration)
        {
            if (client == null) throw new ArgumentNullException("client");
            if (asyncClient == null) throw new ArgumentNullException("asyncClient");
            if (configuration == null) throw new ArgumentNullException("configuration");

            this.Client = client;
            this.AsynchronousClient = asyncClient;
            this.Configuration = configuration;
            this.ExceptionFactory = Org.OpenAPIMuseum.Client.Configuration.DefaultExceptionFactory;
        }

        /// <summary>
        /// The client for accessing this underlying API asynchronously.
        /// </summary>
        public Org.OpenAPIMuseum.Client.IAsynchronousClient AsynchronousClient { get; set; }

        /// <summary>
        /// The client for accessing this underlying API synchronously.
        /// </summary>
        public Org.OpenAPIMuseum.Client.ISynchronousClient Client { get; set; }

        /// <summary>
        /// Gets the base path of the API client.
        /// </summary>
        /// <value>The base path</value>
        public string GetBasePath()
        {
            return this.Configuration.BasePath;
        }

        /// <summary>
        /// Gets or sets the configuration object
        /// </summary>
        /// <value>An instance of the Configuration</value>
        public Org.OpenAPIMuseum.Client.IReadableConfiguration Configuration { get; set; }

        /// <summary>
        /// Provides a factory method hook for the creation of exceptions.
        /// </summary>
        public Org.OpenAPIMuseum.Client.ExceptionFactory ExceptionFactory
        {
            get
            {
                if (_exceptionFactory != null && _exceptionFactory.GetInvocationList().Length > 1)
                {
                    throw new InvalidOperationException("Multicast delegate for ExceptionFactory is unsupported.");
                }
                return _exceptionFactory;
            }
            set { _exceptionFactory = value; }
        }

        /// <summary>
        /// Buy museum tickets Purchase museum tickets for general entry or special events.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>MuseumTicketsConfirmation</returns>
        public MuseumTicketsConfirmation BuyMuseumTickets(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0)
        {
            Org.OpenAPIMuseum.Client.ApiResponse<MuseumTicketsConfirmation> localVarResponse = BuyMuseumTicketsWithHttpInfo(buyMuseumTickets);
            return localVarResponse.Data;
        }

        /// <summary>
        /// Buy museum tickets Purchase museum tickets for general entry or special events.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>ApiResponse of MuseumTicketsConfirmation</returns>
        public Org.OpenAPIMuseum.Client.ApiResponse<MuseumTicketsConfirmation> BuyMuseumTicketsWithHttpInfo(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0)
        {
            // verify the required parameter 'buyMuseumTickets' is set
            if (buyMuseumTickets == null)
            {
                throw new Org.OpenAPIMuseum.Client.ApiException(400, "Missing required parameter 'buyMuseumTickets' when calling TicketsApi->BuyMuseumTickets");
            }

            Org.OpenAPIMuseum.Client.RequestOptions localVarRequestOptions = new Org.OpenAPIMuseum.Client.RequestOptions();

            string[] _contentTypes = new string[] {
                "application/json"
            };

            // to determine the Accept header
            string[] _accepts = new string[] {
                "application/json",
                "application/problem+json"
            };

            var localVarContentType = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderContentType(_contentTypes);
            if (localVarContentType != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Content-Type", localVarContentType);
            }

            var localVarAccept = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderAccept(_accepts);
            if (localVarAccept != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Accept", localVarAccept);
            }

            localVarRequestOptions.Data = buyMuseumTickets;

            localVarRequestOptions.Operation = "TicketsApi.BuyMuseumTickets";
            localVarRequestOptions.OperationIndex = operationIndex;

            // authentication (MuseumPlaceholderAuth) required
            // http basic authentication required
            if (!string.IsNullOrEmpty(this.Configuration.Username) || !string.IsNullOrEmpty(this.Configuration.Password) && !localVarRequestOptions.HeaderParameters.ContainsKey("Authorization"))
            {
                localVarRequestOptions.HeaderParameters.Add("Authorization", "Basic " + Org.OpenAPIMuseum.Client.ClientUtils.Base64Encode(this.Configuration.Username + ":" + this.Configuration.Password));
            }

            // make the HTTP request
            var localVarResponse = this.Client.Post<MuseumTicketsConfirmation>("/tickets", localVarRequestOptions, this.Configuration);
            if (this.ExceptionFactory != null)
            {
                Exception _exception = this.ExceptionFactory("BuyMuseumTickets", localVarResponse);
                if (_exception != null)
                {
                    throw _exception;
                }
            }

            return localVarResponse;
        }

        /// <summary>
        /// Buy museum tickets Purchase museum tickets for general entry or special events.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of MuseumTicketsConfirmation</returns>
        public async System.Threading.Tasks.Task<MuseumTicketsConfirmation> BuyMuseumTicketsAsync(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
        {
            Org.OpenAPIMuseum.Client.ApiResponse<MuseumTicketsConfirmation> localVarResponse = await BuyMuseumTicketsWithHttpInfoAsync(buyMuseumTickets, operationIndex, cancellationToken).ConfigureAwait(false);
            return localVarResponse.Data;
        }

        /// <summary>
        /// Buy museum tickets Purchase museum tickets for general entry or special events.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="buyMuseumTickets"></param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of ApiResponse (MuseumTicketsConfirmation)</returns>
        public async System.Threading.Tasks.Task<Org.OpenAPIMuseum.Client.ApiResponse<MuseumTicketsConfirmation>> BuyMuseumTicketsWithHttpInfoAsync(BuyMuseumTickets buyMuseumTickets, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
        {
            // verify the required parameter 'buyMuseumTickets' is set
            if (buyMuseumTickets == null)
            {
                throw new Org.OpenAPIMuseum.Client.ApiException(400, "Missing required parameter 'buyMuseumTickets' when calling TicketsApi->BuyMuseumTickets");
            }


            Org.OpenAPIMuseum.Client.RequestOptions localVarRequestOptions = new Org.OpenAPIMuseum.Client.RequestOptions();

            string[] _contentTypes = new string[] {
                "application/json"
            };

            // to determine the Accept header
            string[] _accepts = new string[] {
                "application/json",
                "application/problem+json"
            };

            var localVarContentType = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderContentType(_contentTypes);
            if (localVarContentType != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Content-Type", localVarContentType);
            }

            var localVarAccept = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderAccept(_accepts);
            if (localVarAccept != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Accept", localVarAccept);
            }

            localVarRequestOptions.Data = buyMuseumTickets;

            localVarRequestOptions.Operation = "TicketsApi.BuyMuseumTickets";
            localVarRequestOptions.OperationIndex = operationIndex;

            // authentication (MuseumPlaceholderAuth) required
            // http basic authentication required
            if (!string.IsNullOrEmpty(this.Configuration.Username) || !string.IsNullOrEmpty(this.Configuration.Password) && !localVarRequestOptions.HeaderParameters.ContainsKey("Authorization"))
            {
                localVarRequestOptions.HeaderParameters.Add("Authorization", "Basic " + Org.OpenAPIMuseum.Client.ClientUtils.Base64Encode(this.Configuration.Username + ":" + this.Configuration.Password));
            }

            // make the HTTP request
            var localVarResponse = await this.AsynchronousClient.PostAsync<MuseumTicketsConfirmation>("/tickets", localVarRequestOptions, this.Configuration, cancellationToken).ConfigureAwait(false);

            if (this.ExceptionFactory != null)
            {
                Exception _exception = this.ExceptionFactory("BuyMuseumTickets", localVarResponse);
                if (_exception != null)
                {
                    throw _exception;
                }
            }

            return localVarResponse;
        }

        /// <summary>
        /// Get ticket QR code Return an image of your ticket with scannable QR code. Used for event entry.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>System.IO.Stream</returns>
        public System.IO.Stream GetTicketCode(Guid ticketId, int operationIndex = 0)
        {
            Org.OpenAPIMuseum.Client.ApiResponse<System.IO.Stream> localVarResponse = GetTicketCodeWithHttpInfo(ticketId);
            return localVarResponse.Data;
        }

        /// <summary>
        /// Get ticket QR code Return an image of your ticket with scannable QR code. Used for event entry.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <returns>ApiResponse of System.IO.Stream</returns>
        public Org.OpenAPIMuseum.Client.ApiResponse<System.IO.Stream> GetTicketCodeWithHttpInfo(Guid ticketId, int operationIndex = 0)
        {
            Org.OpenAPIMuseum.Client.RequestOptions localVarRequestOptions = new Org.OpenAPIMuseum.Client.RequestOptions();

            string[] _contentTypes = new string[] {
            };

            // to determine the Accept header
            string[] _accepts = new string[] {
                "image/png",
                "application/problem+json"
            };

            var localVarContentType = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderContentType(_contentTypes);
            if (localVarContentType != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Content-Type", localVarContentType);
            }

            var localVarAccept = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderAccept(_accepts);
            if (localVarAccept != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Accept", localVarAccept);
            }

            localVarRequestOptions.PathParameters.Add("ticketId", Org.OpenAPIMuseum.Client.ClientUtils.ParameterToString(ticketId)); // path parameter

            localVarRequestOptions.Operation = "TicketsApi.GetTicketCode";
            localVarRequestOptions.OperationIndex = operationIndex;

            // authentication (MuseumPlaceholderAuth) required
            // http basic authentication required
            if (!string.IsNullOrEmpty(this.Configuration.Username) || !string.IsNullOrEmpty(this.Configuration.Password) && !localVarRequestOptions.HeaderParameters.ContainsKey("Authorization"))
            {
                localVarRequestOptions.HeaderParameters.Add("Authorization", "Basic " + Org.OpenAPIMuseum.Client.ClientUtils.Base64Encode(this.Configuration.Username + ":" + this.Configuration.Password));
            }

            // make the HTTP request
            var localVarResponse = this.Client.Get<System.IO.Stream>("/tickets/{ticketId}/qr", localVarRequestOptions, this.Configuration);
            if (this.ExceptionFactory != null)
            {
                Exception _exception = this.ExceptionFactory("GetTicketCode", localVarResponse);
                if (_exception != null)
                {
                    throw _exception;
                }
            }

            return localVarResponse;
        }

        /// <summary>
        /// Get ticket QR code Return an image of your ticket with scannable QR code. Used for event entry.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of System.IO.Stream</returns>
        public async System.Threading.Tasks.Task<System.IO.Stream> GetTicketCodeAsync(Guid ticketId, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
        {
            Org.OpenAPIMuseum.Client.ApiResponse<System.IO.Stream> localVarResponse = await GetTicketCodeWithHttpInfoAsync(ticketId, operationIndex, cancellationToken).ConfigureAwait(false);
            return localVarResponse.Data;
        }

        /// <summary>
        /// Get ticket QR code Return an image of your ticket with scannable QR code. Used for event entry.
        /// </summary>
        /// <exception cref="Org.OpenAPIMuseum.Client.ApiException">Thrown when fails to make API call</exception>
        /// <param name="ticketId">Identifier for a ticket to a museum event. Used to generate ticket image.</param>
        /// <param name="operationIndex">Index associated with the operation.</param>
        /// <param name="cancellationToken">Cancellation Token to cancel the request.</param>
        /// <returns>Task of ApiResponse (System.IO.Stream)</returns>
        public async System.Threading.Tasks.Task<Org.OpenAPIMuseum.Client.ApiResponse<System.IO.Stream>> GetTicketCodeWithHttpInfoAsync(Guid ticketId, int operationIndex = 0, System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
        {

            Org.OpenAPIMuseum.Client.RequestOptions localVarRequestOptions = new Org.OpenAPIMuseum.Client.RequestOptions();

            string[] _contentTypes = new string[] {
            };

            // to determine the Accept header
            string[] _accepts = new string[] {
                "image/png",
                "application/problem+json"
            };

            var localVarContentType = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderContentType(_contentTypes);
            if (localVarContentType != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Content-Type", localVarContentType);
            }

            var localVarAccept = Org.OpenAPIMuseum.Client.ClientUtils.SelectHeaderAccept(_accepts);
            if (localVarAccept != null)
            {
                localVarRequestOptions.HeaderParameters.Add("Accept", localVarAccept);
            }

            localVarRequestOptions.PathParameters.Add("ticketId", Org.OpenAPIMuseum.Client.ClientUtils.ParameterToString(ticketId)); // path parameter

            localVarRequestOptions.Operation = "TicketsApi.GetTicketCode";
            localVarRequestOptions.OperationIndex = operationIndex;

            // authentication (MuseumPlaceholderAuth) required
            // http basic authentication required
            if (!string.IsNullOrEmpty(this.Configuration.Username) || !string.IsNullOrEmpty(this.Configuration.Password) && !localVarRequestOptions.HeaderParameters.ContainsKey("Authorization"))
            {
                localVarRequestOptions.HeaderParameters.Add("Authorization", "Basic " + Org.OpenAPIMuseum.Client.ClientUtils.Base64Encode(this.Configuration.Username + ":" + this.Configuration.Password));
            }

            // make the HTTP request
            var localVarResponse = await this.AsynchronousClient.GetAsync<System.IO.Stream>("/tickets/{ticketId}/qr", localVarRequestOptions, this.Configuration, cancellationToken).ConfigureAwait(false);

            if (this.ExceptionFactory != null)
            {
                Exception _exception = this.ExceptionFactory("GetTicketCode", localVarResponse);
                if (_exception != null)
                {
                    throw _exception;
                }
            }

            return localVarResponse;
        }

    }
}
