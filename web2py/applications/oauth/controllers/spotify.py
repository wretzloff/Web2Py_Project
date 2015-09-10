import customFunctions
import contextSensitiveFunctions
import httpFunctions
import socket
def index():
    customFunctions.printToLog('------------------------------------------------', 0)
    customFunctions.printToLog('landingPageSpotify()', 1)
    
    #########################
    #Experimental section. Moving logic out of controller and into the Spotify-specific API.
    tempExperimentalFunction()
    #########################
    
    #Get the the Spotify access token from session.
    spotifyAccessToken = contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'Spotify')
    
    #Populate the parameters for the request to the endpoint
    parameterArray = {'access_token' : spotifyAccessToken}
    
    #Build the URL and send the request to that URL
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('adapter_Spotify_me')
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    responseDataInJson = httpFunctions.getRequest(apiURL)
    
    #Parse the response and harvest the data we want.
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)


#Temporary function to experiment with sending HTTP POST.
def tempExperimentalFunction() :
    #Call to the API to get the URL for Sotify's "me" endpoint (https://api.spotify.com/v1/me). 
    configValueApiEndpoint = contextSensitiveFunctions.getApiEndpoint('getConfigValue', None)
    parameterArray = {'resourceOwner' : 'Spotify',
                      'configSetting' : 'me_endpoint'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    urlOfSpotifyMeEndpoint = httpFunctions.getRequest(apiURL)
    
    #Get the the Spotify access token from session.
    spotifyAccessToken = contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'Spotify')
    
    #Populate the parameters for the request to the endpoint
    jsonStringParameters = {'dummyHTTPPOSTParameter1' : 'dummyHTTPPOSTValue1',
                      'dummyHTTPPOSTParameter2' : 'dummyHTTPPOSTValue2'}
    jsonString = httpFunctions.convertArrayToJson(jsonStringParameters)
    parameterArray = {'access_token' : spotifyAccessToken,
                      'resourceOwnerUrl' : urlOfSpotifyMeEndpoint,
                      'jsonString' : jsonString}
    
    #Build the URL and send the request to that URL
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('generateAuthenticatedRequestToUrl')
    response = httpFunctions.postRequest(apiEndpoint, parameterArray, None)
    print response.read()
