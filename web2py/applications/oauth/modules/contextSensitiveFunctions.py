import customFunctions
import httpFunctions
import socket

#Configuration point. Function to fetch the specified API endpoint.
def getApiEndpoint(endpoint, resourceOwner = None) :
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + '/oauth/api/' + endpoint
    return apiEndpoint

#Configuration point. Function to fetch the standard redirect URI.
def getRedirectUri() :
    return 'http://127.0.0.1:8000/oauth'

#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorization(resourceOwner) :
    #Define the redirect_uri that we want the Resource Owner to redirect to once the user has logged in.
    redirect_uri = getRedirectUri()
    
    #Call the API endpoint to generate a return a URL
    apiEndpoint = getApiEndpoint('buildUrlToInitiateAuthorization', None)
    parameterArray = {'resourceOwner' : resourceOwner,
                      'oAuthRedirectUri' : redirect_uri}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    full_url = httpFunctions.getRequest(apiURL)
    return full_url


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
