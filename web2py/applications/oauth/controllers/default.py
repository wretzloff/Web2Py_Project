#Todo: service-enable functions in modules.
#Todo: convert to use applications\oauth\views\spotify\index instead of applications\oauth\views\default\landingPageSpotify
#Todo: postToTokenEndpoint() hardcodes the grant_type
import customFunctions
import contextSensitiveFunctions
import httpFunctions
import oauthFunctions
def index():
    customFunctions.printToLog('------------------------------------------------')
    customFunctions.printToLog('index()')
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    parameterCode = request.vars['code']
    parameterError = request.vars['error']
    if parameterError is not None:
        customFunctions.printToLog('URL parameter \'error\': ' + parameterError)
    elif parameterCode is not None:
        #Generate an HTTP POST to the "token" endpoint and save the results to the session.
        customFunctions.printToLog('URL parameter \'code\': ' + parameterCode)
        postToTokenEndpointAuthorizationCodeSpotify(parameterCode)
        #Now that the Access Token has been saved to session, redirect the the landing page for this resource.
        redirect(URL('landingPageSpotify'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = buildUrlToInitiateAuthorizationSpotify()
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)


def landingPageSpotify():
    customFunctions.printToLog('------------------------------------------------')
    customFunctions.printToLog('landingPageSpotify()')
    url = contextSensitiveFunctions.getConfigValue('Spotify','me_endpoint',db)
    authorizationHeader = 'Bearer ' + contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'spotify')
    headers = {'Authorization' : authorizationHeader}
    responseDataInJson = httpFunctions.getRequest(url, None, headers)
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)
    
#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorizationSpotify() :
    url = contextSensitiveFunctions.getConfigValue('Spotify','authorization_endpoint',db)
    client_id = contextSensitiveFunctions.getConfigValue('Spotify','client_id',db)
    response_type = contextSensitiveFunctions.getConfigValue('Spotify','response_type',db)
    redirect_uri = contextSensitiveFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    scope = contextSensitiveFunctions.getConfigValue('Spotify','scopes',db)
    show_dialog = contextSensitiveFunctions.getConfigValue('Spotify','show_dialog',db)
    #Build full URL
    full_url = oauthFunctions.buildUrlToInitiateAuthorization(url, client_id, response_type, redirect_uri, scope, show_dialog)
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    postUrl = contextSensitiveFunctions.getConfigValue('Spotify','token_endpoint',db)
    redirect_uri = contextSensitiveFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    client_id = contextSensitiveFunctions.getConfigValue('Spotify','client_id',db)
    client_secret = contextSensitiveFunctions.getConfigValue('Spotify','client_secret',db)
    responseDataInArray = oauthFunctions.postToTokenEndpoint(postUrl, codeParameterForPostRequest, redirect_uri, client_id, client_secret)
    contextSensitiveFunctions.addOauthSessionVariable(session, 'access_token', responseDataInArray['access_token'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'token_type', responseDataInArray['token_type'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'expires_in', responseDataInArray['expires_in'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'refresh_token', responseDataInArray['refresh_token'], 'spotify')
