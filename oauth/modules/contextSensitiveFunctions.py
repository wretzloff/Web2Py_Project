import customFunctions
import httpFunctions
import socket

###############################################################################################################################
###############################################################################################################################
####Configuration

#Configuration point. Function to fetch the specified API endpoint.
def getApiEndpoint(endpoint, resourceOwner = None) :
    application = 'oauth'
    controller = 'api' + (resourceOwner or '')
    
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000/' + application + '/' + controller + '/' + endpoint
    return apiEndpoint

#Configuration point. Function to fetch the standard redirect URI.
def getRedirectUri() :
    return 'http://127.0.0.1:8000/oauth'

###############################################################################################################################
###############################################################################################################################
####Reusable helper functions.

#Helper function to take a Resource Owner and communicate with the API to get the URI that is used to initiate authorization for this Resource Owner.
def callBuildUrlToInitiateAuthorization(resourceOwner) :
    #Define the redirect_uri that we want the Resource Owner to redirect to once the user has logged in.
    redirect_uri = getRedirectUri()
    
    #Call the API endpoint to generate a return a URL
    apiEndpoint = getApiEndpoint('buildUrlToInitiateAuthorization', None)
    parameterArray = {'resourceOwner' : resourceOwner,
                      'oAuthRedirectUri' : redirect_uri}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    full_url = httpFunctions.getRequest(apiURL)
    return full_url

#Helper function to take a Resource Owner and an oAuth authorization code, and then communicate with the API to have an HTTP POST request sent to that Resource Owner's designated endpoint to receive an Access Token. The Access Token, along with some other data, will be returned to the caller.
def callPostToTokenEndpointAuthorizationCode(resourceOwner, authorizationCode) :
    #Define the redirect_uri that we want the Resource Owner to redirect to once the user has logged in.
    redirect_uri = getRedirectUri()
    
    #Call the API endpoint to send an HTTP POST request and return the response data to us.
    apiEndpoint = getApiEndpoint('postToTokenEndpointAuthorizationCode', None)
    parameterArray = {'resourceOwner' : resourceOwner,
                      'codeParameterForPostRequest' : authorizationCode,
                      'oAuthRedirectUri' : redirect_uri}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    responseDataInJson = httpFunctions.getRequest(apiURL)
    #Convert JSON string to an array
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    return responseDataInArray

###############################################################################################################################
###############################################################################################################################
####Functions for manipulating session variables.

#Function to add the designated session variable to session.
#Session: the session to add a variable to.
#oAuthVariableType: designates what type of variable we are adding.
#value: value that the variable will hold.
#resourceOwner: designates which resource owner this variable is for, i.e. Spotify, Facebook, etc.
def addOauthSessionVariable(session, oAuthVariableType, value, resourceOwner = None) :
	customFunctions.printToLog('addOauthSessionVariable: oAuthVariableType: ' + str(oAuthVariableType), 0)
	customFunctions.printToLog('addOauthSessionVariable: resourceOwner: ' + str(resourceOwner), 0)
	customFunctions.printToLog('addOauthSessionVariable: value: ' + str(value), 1)
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
		customFunctions.printToLog('addOauthSessionVariable: error', 1)

#Function to get the designated session variable from session.
#Session: the session to add a variable to.
#oAuthVariableType: designates what type of variable we are adding.
#resourceOwner: designates which resource owner this variable is for, i.e. Spotify, Facebook, etc.
def getOauthSessionVariable(session, oAuthVariableType, resourceOwner = None) :
	customFunctions.printToLog('getOauthSessionVariable: oAuthVariableType: ' + str(oAuthVariableType), 0)
	customFunctions.printToLog('getOauthSessionVariable: resourceOwner: ' + str(resourceOwner), 0)
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
	customFunctions.printToLog('getOauthSessionVariable: returnValue: ' + str(returnValue), 1)
	return returnValue
