#Todo: logging for the function postRequest()
#Todo: service-enable functions in oauthFunctions module. customFunctions, contextSensitiveFunctions, and httpFunctions modules are not business logic and so don't need to be exposed as a web service.
#Todo: move functionlity of fetching Resource Owner info to the API.
#Todo: put a generic version of buildUrlToInitiateAuthorizationSpotify() and postToTokenEndpointAuthorizationCodeSpotify() in the contextSensitiveFunctions module that will take in a Ressource Owner name, fetch necessary configuration data from database, perform business logic, and store appropriate data to session. They will go in contextSensitiveFunctions module because they are not standalone functions - they are convenience functions.
import customFunctions
import contextSensitiveFunctions
import httpFunctions
import oauthFunctions
import socket
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
        redirect(URL('spotify', 'index'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = buildUrlToInitiateAuthorizationSpotify()
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)
    
#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorizationSpotify() :
    #Get configuration values
    url = contextSensitiveFunctions.getConfigValue('Spotify','authorization_endpoint',db)
    client_id = contextSensitiveFunctions.getConfigValue('Spotify','client_id',db)
    response_type = contextSensitiveFunctions.getConfigValue('Spotify','response_type',db)
    redirect_uri = contextSensitiveFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    scope = contextSensitiveFunctions.getConfigValue('Spotify','scopes',db)
    show_dialog = contextSensitiveFunctions.getConfigValue('Spotify','show_dialog',db)
    
    #Call the API endpoint to generate a return a URL
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','buildUrlToInitiateAuthorization')
    parameterArray = {'authorization_endpoint' : url,
                      'client_id' : client_id,
                      'response_type' : response_type,
                      'oAuthRedirectUri' : redirect_uri,
                      'scopes' : scope,
                      'show_dialog' : show_dialog}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    full_url = httpFunctions.getRequest(apiURL)
    
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    #Get configuration values
    postUrl = contextSensitiveFunctions.getConfigValue('Spotify','token_endpoint',db)
    redirect_uri = contextSensitiveFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    client_id = contextSensitiveFunctions.getConfigValue('Spotify','client_id',db)
    client_secret = contextSensitiveFunctions.getConfigValue('Spotify','client_secret',db)
    ###################################################################################
    #Call the API endpoint to send an HTTP POST request and return the response data to us.
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','postToTokenEndpointAuthorizationCode')
    parameterArray = {'postUrl' : postUrl,
                      'codeParameterForPostRequest' : codeParameterForPostRequest,
                      'oAuthRedirectUri' : redirect_uri,
                      'client_id' : client_id,
                      'client_secret' : client_secret}
    #apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    #print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' + apiURL
    #responseDataInJson = httpFunctions.getRequest(apiURL)
    #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + responseDataInJson
    #responseDataInArray2 = httpFunctions.convertJsonToArray(responseDataInJson)
    #print 'cccccccccccccccccccccccccccccccccccccccccccccccccccccc' + responseDataInArray['access_token']
    ###################################################################################
    responseDataInArray = oauthFunctions.postToTokenEndpointAuthorizationCode(postUrl, codeParameterForPostRequest, redirect_uri, client_id, client_secret)
    contextSensitiveFunctions.addOauthSessionVariable(session, 'access_token', responseDataInArray['access_token'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'token_type', responseDataInArray['token_type'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'expires_in', responseDataInArray['expires_in'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'refresh_token', responseDataInArray['refresh_token'], 'spotify')
