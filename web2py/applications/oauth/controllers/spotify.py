import customFunctions
import contextSensitiveFunctions
import httpFunctions
import socket
def index():
    customFunctions.printToLog('------------------------------------------------', 0)
    customFunctions.printToLog('landingPageSpotify()', 1)
    
    #Get the user's email address
    authorizedUserEmailAddress = helperGetUserEmailAddress()
    
    #Get the user's saved tracks
    savedTracks = helperGetSavedTracks()
    
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress, savedTracks = savedTracks)


#Helper function to get the user's logged-in email address.
def helperGetUserEmailAddress() :
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
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('sendGetToUrl')
    response = httpFunctions.postRequest(apiEndpoint, parameterArray, None)
    responseDataInJson = response.read()
    
    #Parse the response and harvest the data we want.
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    return responseDataInArray['email']

#Helper function to get the user's logged-in email address.
def helperGetSavedTracks() :
    #Get Spotify's "me/tracks" endpoint (https://api.spotify.com/v1/me/tracks).
    urlOfSpotifyMeEndpoint = 'https://api.spotify.com/v1/me/tracks'
    
    #Get the the Spotify access token from session.
    spotifyAccessToken = contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'Spotify')
    
    #Populate the parameters for the request to the endpoint
    parameterArray = {'access_token' : spotifyAccessToken,
                      'resourceOwnerUrl' : urlOfSpotifyMeEndpoint}
    
    #Build the URL and send the request to that URL
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('sendGetToUrl')
    response = httpFunctions.postRequest(apiEndpoint, parameterArray, None)
    responseDataInJson = response.read()
    
    #Parse the response and harvest the data we want.
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    songsArray = responseDataInArray['items']
    #Loop through the saved tracks and save off the data that we want.
    tracksArray = []
    for s in songsArray:
        row = {}
        row['name'] = s['track']['name']
        row['added_at'] = s['added_at']
        row['artist'] = s['track']['artists'][0]['name']
        row['album'] = s['track']['album']['name']
        tracksArray.insert(0,row)
    
    return tracksArray
