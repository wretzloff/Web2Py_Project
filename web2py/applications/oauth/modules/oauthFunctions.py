import httpFunctions
import customFunctions

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

	
#Helper function to send an HTTP POST request to the /token endpoint
def postToTokenEndpoint(postUrl,codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret) :
    requestBodyParameters = {'grant_type' : 'authorization_code',
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

def addOauthSessionVariable(session, oAuthVariableType, value, resourceOwner = None) :
	customFunctions.printToLog('addOauthSessionVariable: oAuthVariableType: ' + str(oAuthVariableType))
	customFunctions.printToLog('addOauthSessionVariable: resourceOwner: ' + str(resourceOwner))
	customFunctions.printToLog('addOauthSessionVariable: value: ' + str(value))
	if oAuthVariableType == 'access_token':
		session.access_token = session.access_token or {}
		session.access_token[resourceOwner] = value
	elif oAuthVariableType == 'token_type':
		session.token_type = session.token_type or {}
		session.token_type[resourceOwner] = value
	elif oAuthVariableType == 'expires_in':
		session.expires_in = session.expires_in or {}
		session.expires_in[resourceOwner] = value
	elif oAuthVariableType == 'refresh_token':
		session.refresh_token = session.refresh_token or {}
		session.refresh_token[resourceOwner] = value	
	else:
		print 'error'

def getOauthSessionVariable(session, oAuthVariableType, resourceOwner = None) :
	customFunctions.printToLog('getOauthSessionVariable: oAuthVariableType: ' + str(oAuthVariableType))
	customFunctions.printToLog('getOauthSessionVariable: resourceOwner: ' + str(resourceOwner))
	if oAuthVariableType == 'access_token':
		session.access_token = session.access_token or {}
		returnValue = session.access_token[resourceOwner]
	elif oAuthVariableType == 'token_type':
		session.token_type = session.token_type or {}
		returnValue = session.token_type[resourceOwner]
	elif oAuthVariableType == 'expires_in':
		session.expires_in = session.expires_in or {}
		returnValue = session.expires_in[resourceOwner]
	elif oAuthVariableType == 'refresh_token':
		session.refresh_token = session.refresh_token or {}
		returnValue = session.refresh_token[resourceOwner]
	else:
		returnValue = None
	customFunctions.printToLog('getOauthSessionVariable: returnValue: ' + str(returnValue))
	return returnValue