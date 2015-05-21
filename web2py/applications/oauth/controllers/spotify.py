import customFunctions
import contextSensitiveFunctions
import httpFunctions
import socket
def index():
    customFunctions.printToLog('------------------------------------------------', 0)
    customFunctions.printToLog('landingPageSpotify()', 1)
    #########################
    #Experimental section. Moving logic out of controller and into the Spotify-specific API.
    callMeEndpoint()
    #########################
    
    #Define the path to the API endpoint to fetch a configuration value
    configValueApiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','getConfigValue')
    
    #Get me_endpoint config value
    parameterArray = {'resourceOwner' : 'Spotify',
                      'configSetting' : 'me_endpoint'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    url = httpFunctions.getRequest(apiURL)
    
    authorizationHeader = 'Bearer ' + contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'Spotify')
    headers = {'Authorization' : authorizationHeader}
    responseDataInJson = httpFunctions.getRequest(url, None, headers)
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)


#Helper function......................
def callMeEndpoint() :
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('testEndpoint', 'Spotify')
    #parameterArray = {'resourceOwner' : resourceOwner,
    #                  'oAuthRedirectUri' : redirect_uri}
    #apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    #full_url = httpFunctions.getRequest(apiURL)
    #return full_url
