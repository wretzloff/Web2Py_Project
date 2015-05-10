#Todo: comprehensive error handling
#Todo: put a generic version of buildUrlToInitiateAuthorizationSpotify() and postToTokenEndpointAuthorizationCodeSpotify() in the contextSensitiveFunctions module that will take in a Ressource Owner name, fetch necessary configuration data from database, perform business logic, and store appropriate data to session. They will go in contextSensitiveFunctions module because they are not standalone functions - they are convenience functions.
#Todo: update Spotify page controller to call API to get data, instead of calling Spotify directly.
import customFunctions
import contextSensitiveFunctions
import httpFunctions
def index():
    customFunctions.printToLog('------------------------------------------------', 0)
    customFunctions.printToLog('index()', 0)
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    parameterCode = request.vars['code']
    parameterError = request.vars['error']
    if parameterError is not None:
        customFunctions.printToLog('URL parameter \'error\': ' + parameterError, 1)
    elif parameterCode is not None:
        #Generate an HTTP POST to the "token" endpoint and save the results to the session.
        customFunctions.printToLog('URL parameter \'code\': ' + parameterCode, 1)
        postToTokenEndpointAuthorizationCode('Spotify', parameterCode)
        #Now that the Access Token has been saved to session, redirect the the landing page for this resource.
        redirect(URL('spotify', 'index'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = contextSensitiveFunctions.buildUrlToInitiateAuthorization('Spotify')
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCode(resourceOwner, codeParameterForPostRequest) :
    #Define the redirect_uri that we want the Resource Owner to redirect to once the user has logged in.
    redirect_uri = contextSensitiveFunctions.getRedirectUri()
    
    #Call the API endpoint to send an HTTP POST request and return the response data to us.
    apiEndpoint = contextSensitiveFunctions.getApiEndpoint('postToTokenEndpointAuthorizationCode', None)
    parameterArray = {'resourceOwner' : resourceOwner,
                      'codeParameterForPostRequest' : codeParameterForPostRequest,
                      'oAuthRedirectUri' : redirect_uri}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    responseDataInJson = httpFunctions.getRequest(apiURL)
    #Convert JSON string to an array
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    #Store data to session
    contextSensitiveFunctions.addOauthSessionVariable(session, 'access_token', responseDataInArray['access_token'], resourceOwner)
    contextSensitiveFunctions.addOauthSessionVariable(session, 'token_type', responseDataInArray['token_type'], resourceOwner)
    contextSensitiveFunctions.addOauthSessionVariable(session, 'expires_in', responseDataInArray['expires_in'], resourceOwner)
    contextSensitiveFunctions.addOauthSessionVariable(session, 'refresh_token', responseDataInArray['refresh_token'], resourceOwner)
