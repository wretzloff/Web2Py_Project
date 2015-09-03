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
    
    #Define the URL of the API endpoint that we can call to fetch a configuration value
    configValueApiEndpoint = contextSensitiveFunctions.getApiEndpoint('getConfigValue', None)
    
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


#Helper function to communicate with the adapter_Spotify_me endpoint of the API.
def callMeEndpoint() :
    #Get the the Spotify access token from session.
    spotifyAccessToken = contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'Spotify')
    
    #Populate the parameters for the request to the endpoint
    parameterArray = {'access_token' : spotifyAccessToken}
    
    #Build the URL and send the request to that URL
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('adapter_Spotify_me')
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    response = httpFunctions.getRequest(apiURL)
    print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + response
