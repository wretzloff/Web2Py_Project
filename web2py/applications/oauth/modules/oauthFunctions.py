import customFunctions
import httpFunctions

#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorization(authorization_endpoint,client_id, response_type, oAuthRedirectUri, scopes,show_dialog) :
    #Define parameters
    data = {}
    data['client_id'] = client_id
    data['response_type'] = response_type
    data['redirect_uri'] = oAuthRedirectUri
    data['scope'] = scopes
    data['show_dialog'] = show_dialog
    #Build full URL
    full_url = httpFunctions.buildFullUrl(authorization_endpoint, data)
    return full_url

	
#Helper function to send an HTTP POST request to the /token endpoint using the 'authorization_code' Grant Type.
def postToTokenEndpointAuthorizationCode(postUrl, codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret) :
	return postToTokenEndpoint(postUrl, 'authorization_code', codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret)
	
#Helper function to send an HTTP POST request to the /token endpoint
def postToTokenEndpoint(postUrl, grantType, codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret) :
    requestBodyParameters = {'grant_type' : grantType,
                             'code' : codeParameterForPostRequest,
                             'redirect_uri' : oAuthRedirectUri,
                             'client_id' : client_id,
                             'client_secret' : client_secret}
    #Call the function to send the HTTP POST and get the response
    responseFromPost = httpFunctions.postRequest(postUrl, requestBodyParameters)
    #Parse the response and return the data to the caller.
    responseDataInJson = responseFromPost.read()
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    customFunctions.printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray))
    return responseDataInArray