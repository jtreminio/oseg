/*
 * Redocly Museum API
 * Imaginary, but delightful Museum API for interacting with museum services and information. Built with love by Redocly.
 *
 * The version of the OpenAPI document: 1.2.1
 * Contact: team@redocly.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


package org.openapimuseum.client.api;

import org.openapimuseum.client.ApiCallback;
import org.openapimuseum.client.ApiClient;
import org.openapimuseum.client.ApiException;
import org.openapimuseum.client.ApiResponse;
import org.openapimuseum.client.Configuration;
import org.openapimuseum.client.Pair;
import org.openapimuseum.client.ProgressRequestBody;
import org.openapimuseum.client.ProgressResponseBody;

import com.google.gson.reflect.TypeToken;

import java.io.IOException;


import org.openapimuseum.client.model.BuyMuseumTickets;
import org.openapimuseum.client.model.Error;
import java.io.File;
import org.openapimuseum.client.model.MuseumTicketsConfirmation;
import java.util.UUID;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TicketsApi {
    private ApiClient localVarApiClient;
    private int localHostIndex;
    private String localCustomBaseUrl;

    public TicketsApi() {
        this(Configuration.getDefaultApiClient());
    }

    public TicketsApi(ApiClient apiClient) {
        this.localVarApiClient = apiClient;
    }

    public ApiClient getApiClient() {
        return localVarApiClient;
    }

    public void setApiClient(ApiClient apiClient) {
        this.localVarApiClient = apiClient;
    }

    public int getHostIndex() {
        return localHostIndex;
    }

    public void setHostIndex(int hostIndex) {
        this.localHostIndex = hostIndex;
    }

    public String getCustomBaseUrl() {
        return localCustomBaseUrl;
    }

    public void setCustomBaseUrl(String customBaseUrl) {
        this.localCustomBaseUrl = customBaseUrl;
    }

    /**
     * Build call for buyMuseumTickets
     * @param buyMuseumTickets  (required)
     * @param _callback Callback for upload/download progress
     * @return Call to execute
     * @throws ApiException If fail to serialize the request body object
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 201 </td><td> Created. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public okhttp3.Call buyMuseumTicketsCall(BuyMuseumTickets buyMuseumTickets, final ApiCallback _callback) throws ApiException {
        String basePath = null;
        // Operation Servers
        String[] localBasePaths = new String[] {  };

        // Determine Base Path to Use
        if (localCustomBaseUrl != null){
            basePath = localCustomBaseUrl;
        } else if ( localBasePaths.length > 0 ) {
            basePath = localBasePaths[localHostIndex];
        } else {
            basePath = null;
        }

        Object localVarPostBody = buyMuseumTickets;

        // create path and map variables
        String localVarPath = "/tickets";

        List<Pair> localVarQueryParams = new ArrayList<Pair>();
        List<Pair> localVarCollectionQueryParams = new ArrayList<Pair>();
        Map<String, String> localVarHeaderParams = new HashMap<String, String>();
        Map<String, String> localVarCookieParams = new HashMap<String, String>();
        Map<String, Object> localVarFormParams = new HashMap<String, Object>();

        final String[] localVarAccepts = {
            "application/json",
            "application/problem+json"
        };
        final String localVarAccept = localVarApiClient.selectHeaderAccept(localVarAccepts);
        if (localVarAccept != null) {
            localVarHeaderParams.put("Accept", localVarAccept);
        }

        final String[] localVarContentTypes = {
            "application/json"
        };
        final String localVarContentType = localVarApiClient.selectHeaderContentType(localVarContentTypes);
        if (localVarContentType != null) {
            localVarHeaderParams.put("Content-Type", localVarContentType);
        }

        String[] localVarAuthNames = new String[] { "MuseumPlaceholderAuth" };
        return localVarApiClient.buildCall(basePath, localVarPath, "POST", localVarQueryParams, localVarCollectionQueryParams, localVarPostBody, localVarHeaderParams, localVarCookieParams, localVarFormParams, localVarAuthNames, _callback);
    }

    @SuppressWarnings("rawtypes")
    private okhttp3.Call buyMuseumTicketsValidateBeforeCall(BuyMuseumTickets buyMuseumTickets, final ApiCallback _callback) throws ApiException {
        // verify the required parameter 'buyMuseumTickets' is set
        if (buyMuseumTickets == null) {
            throw new ApiException("Missing the required parameter 'buyMuseumTickets' when calling buyMuseumTickets(Async)");
        }

        return buyMuseumTicketsCall(buyMuseumTickets, _callback);

    }

    /**
     * Buy museum tickets
     * Purchase museum tickets for general entry or special events.
     * @param buyMuseumTickets  (required)
     * @return MuseumTicketsConfirmation
     * @throws ApiException If fail to call the API, e.g. server error or cannot deserialize the response body
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 201 </td><td> Created. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public MuseumTicketsConfirmation buyMuseumTickets(BuyMuseumTickets buyMuseumTickets) throws ApiException {
        ApiResponse<MuseumTicketsConfirmation> localVarResp = buyMuseumTicketsWithHttpInfo(buyMuseumTickets);
        return localVarResp.getData();
    }

    /**
     * Buy museum tickets
     * Purchase museum tickets for general entry or special events.
     * @param buyMuseumTickets  (required)
     * @return ApiResponse&lt;MuseumTicketsConfirmation&gt;
     * @throws ApiException If fail to call the API, e.g. server error or cannot deserialize the response body
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 201 </td><td> Created. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public ApiResponse<MuseumTicketsConfirmation> buyMuseumTicketsWithHttpInfo(BuyMuseumTickets buyMuseumTickets) throws ApiException {
        okhttp3.Call localVarCall = buyMuseumTicketsValidateBeforeCall(buyMuseumTickets, null);
        Type localVarReturnType = new TypeToken<MuseumTicketsConfirmation>(){}.getType();
        return localVarApiClient.execute(localVarCall, localVarReturnType);
    }

    /**
     * Buy museum tickets (asynchronously)
     * Purchase museum tickets for general entry or special events.
     * @param buyMuseumTickets  (required)
     * @param _callback The callback to be executed when the API call finishes
     * @return The request call
     * @throws ApiException If fail to process the API call, e.g. serializing the request body object
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 201 </td><td> Created. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public okhttp3.Call buyMuseumTicketsAsync(BuyMuseumTickets buyMuseumTickets, final ApiCallback<MuseumTicketsConfirmation> _callback) throws ApiException {

        okhttp3.Call localVarCall = buyMuseumTicketsValidateBeforeCall(buyMuseumTickets, _callback);
        Type localVarReturnType = new TypeToken<MuseumTicketsConfirmation>(){}.getType();
        localVarApiClient.executeAsync(localVarCall, localVarReturnType, _callback);
        return localVarCall;
    }
    /**
     * Build call for getTicketCode
     * @param ticketId Identifier for a ticket to a museum event. Used to generate ticket image. (required)
     * @param _callback Callback for upload/download progress
     * @return Call to execute
     * @throws ApiException If fail to serialize the request body object
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 200 </td><td> Scannable event ticket in image format. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public okhttp3.Call getTicketCodeCall(UUID ticketId, final ApiCallback _callback) throws ApiException {
        String basePath = null;
        // Operation Servers
        String[] localBasePaths = new String[] {  };

        // Determine Base Path to Use
        if (localCustomBaseUrl != null){
            basePath = localCustomBaseUrl;
        } else if ( localBasePaths.length > 0 ) {
            basePath = localBasePaths[localHostIndex];
        } else {
            basePath = null;
        }

        Object localVarPostBody = null;

        // create path and map variables
        String localVarPath = "/tickets/{ticketId}/qr"
            .replace("{" + "ticketId" + "}", localVarApiClient.escapeString(ticketId.toString()));

        List<Pair> localVarQueryParams = new ArrayList<Pair>();
        List<Pair> localVarCollectionQueryParams = new ArrayList<Pair>();
        Map<String, String> localVarHeaderParams = new HashMap<String, String>();
        Map<String, String> localVarCookieParams = new HashMap<String, String>();
        Map<String, Object> localVarFormParams = new HashMap<String, Object>();

        final String[] localVarAccepts = {
            "image/png",
            "application/problem+json"
        };
        final String localVarAccept = localVarApiClient.selectHeaderAccept(localVarAccepts);
        if (localVarAccept != null) {
            localVarHeaderParams.put("Accept", localVarAccept);
        }

        final String[] localVarContentTypes = {
        };
        final String localVarContentType = localVarApiClient.selectHeaderContentType(localVarContentTypes);
        if (localVarContentType != null) {
            localVarHeaderParams.put("Content-Type", localVarContentType);
        }

        String[] localVarAuthNames = new String[] { "MuseumPlaceholderAuth" };
        return localVarApiClient.buildCall(basePath, localVarPath, "GET", localVarQueryParams, localVarCollectionQueryParams, localVarPostBody, localVarHeaderParams, localVarCookieParams, localVarFormParams, localVarAuthNames, _callback);
    }

    @SuppressWarnings("rawtypes")
    private okhttp3.Call getTicketCodeValidateBeforeCall(UUID ticketId, final ApiCallback _callback) throws ApiException {
        // verify the required parameter 'ticketId' is set
        if (ticketId == null) {
            throw new ApiException("Missing the required parameter 'ticketId' when calling getTicketCode(Async)");
        }

        return getTicketCodeCall(ticketId, _callback);

    }

    /**
     * Get ticket QR code
     * Return an image of your ticket with scannable QR code. Used for event entry.
     * @param ticketId Identifier for a ticket to a museum event. Used to generate ticket image. (required)
     * @return File
     * @throws ApiException If fail to call the API, e.g. server error or cannot deserialize the response body
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 200 </td><td> Scannable event ticket in image format. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public File getTicketCode(UUID ticketId) throws ApiException {
        ApiResponse<File> localVarResp = getTicketCodeWithHttpInfo(ticketId);
        return localVarResp.getData();
    }

    /**
     * Get ticket QR code
     * Return an image of your ticket with scannable QR code. Used for event entry.
     * @param ticketId Identifier for a ticket to a museum event. Used to generate ticket image. (required)
     * @return ApiResponse&lt;File&gt;
     * @throws ApiException If fail to call the API, e.g. server error or cannot deserialize the response body
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 200 </td><td> Scannable event ticket in image format. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public ApiResponse<File> getTicketCodeWithHttpInfo(UUID ticketId) throws ApiException {
        okhttp3.Call localVarCall = getTicketCodeValidateBeforeCall(ticketId, null);
        Type localVarReturnType = new TypeToken<File>(){}.getType();
        return localVarApiClient.execute(localVarCall, localVarReturnType);
    }

    /**
     * Get ticket QR code (asynchronously)
     * Return an image of your ticket with scannable QR code. Used for event entry.
     * @param ticketId Identifier for a ticket to a museum event. Used to generate ticket image. (required)
     * @param _callback The callback to be executed when the API call finishes
     * @return The request call
     * @throws ApiException If fail to process the API call, e.g. serializing the request body object
     * @http.response.details
     <table summary="Response Details" border="1">
        <tr><td> Status Code </td><td> Description </td><td> Response Headers </td></tr>
        <tr><td> 200 </td><td> Scannable event ticket in image format. </td><td>  -  </td></tr>
        <tr><td> 400 </td><td>  </td><td>  -  </td></tr>
        <tr><td> 404 </td><td>  </td><td>  -  </td></tr>
     </table>
     */
    public okhttp3.Call getTicketCodeAsync(UUID ticketId, final ApiCallback<File> _callback) throws ApiException {

        okhttp3.Call localVarCall = getTicketCodeValidateBeforeCall(ticketId, _callback);
        Type localVarReturnType = new TypeToken<File>(){}.getType();
        localVarApiClient.executeAsync(localVarCall, localVarReturnType, _callback);
        return localVarCall;
    }
}
