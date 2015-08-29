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


#Helper function to communicate with the callMeEndpoint of the Spotify-specific API.
def callMeEndpoint() :
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('callMeEndpoint', 'Spotify')
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, None)
