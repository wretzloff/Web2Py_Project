#Todo: split postToTokenEndpointAuthorizationCode(): store session variables separately.
#Todo: comprehensive error handling
#Todo: update Spotify page controller to call API to get data, instead of calling Spotify directly.
import customFunctions
import contextSensitiveFunctions
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
        contextSensitiveFunctions.postToTokenEndpointAuthorizationCode('Spotify', parameterCode, session)
        #Now that the Access Token has been saved to session, redirect the the landing page for this resource.
        redirect(URL('spotify', 'index'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = contextSensitiveFunctions.buildUrlToInitiateAuthorization('Spotify')
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)
