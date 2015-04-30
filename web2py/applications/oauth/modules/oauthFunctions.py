import customFunctions
import httpFunctions
	
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