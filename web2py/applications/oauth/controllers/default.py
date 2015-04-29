#Todo: more elegant solution needed in getConfigValue() API endpoint.
#Todo: logging for the function postRequest()
#Todo: move functionlity of fetching Resource Owner info to the API.
#Todo: put a generic version of buildUrlToInitiateAuthorizationSpotify() and postToTokenEndpointAuthorizationCodeSpotify() in the contextSensitiveFunctions module that will take in a Ressource Owner name, fetch necessary configuration data from database, perform business logic, and store appropriate data to session. They will go in contextSensitiveFunctions module because they are not standalone functions - they are convenience functions.
import customFunctions
import contextSensitiveFunctions
import httpFunctions
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
    #Define the redirect_uri that we want the Resource Owner to redirect to once the user has logged in.
    redirect_uri = 'http://127.0.0.1:8000/oauth'
    #redirect_uri = 'http://127.0.0.1:8000' + URL(None,'oauth',None)
    
    #Call the API endpoint to generate a return a URL
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','buildUrlToInitiateAuthorization')
    parameterArray = {'resourceOwner' : 'Spotify',
                      'oAuthRedirectUri' : redirect_uri}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    full_url = httpFunctions.getRequest(apiURL)
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    #Define the path to the API endpoint to fetch a configuration value
    configValueApiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','getConfigValue')

    #Get token_endpoint config value
    parameterArray = {'resourceOwner' : 'Spotify',
                      'configSetting' : 'token_endpoint'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    postUrl = httpFunctions.getRequest(apiURL)
    
    #Get the oAuthRedirectUri config value
    parameterArray = {'resourceOwner' : None,
                      'configSetting' : 'oAuthRedirectUri'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    redirect_uri = httpFunctions.getRequest(apiURL)
    
    #Get the client_id config value
    parameterArray = {'resourceOwner' : 'Spotify',
                      'configSetting' : 'client_id'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    client_id = httpFunctions.getRequest(apiURL)
    
    #Get the client_secret config value
    parameterArray = {'resourceOwner' : 'Spotify',
                      'configSetting' : 'client_secret'}
    apiURL = httpFunctions.buildFullUrl(configValueApiEndpoint, parameterArray)
    client_secret = httpFunctions.getRequest(apiURL)
    
    #Call the API endpoint to send an HTTP POST request and return the response data to us.
    apiEndpoint = 'http://' + socket.gethostbyname(socket.gethostname()) + ':8000' + URL(None,'api','postToTokenEndpointAuthorizationCode')
    parameterArray = {'resourceOwner' : 'Spotify',
                      'postUrl' : postUrl,
                      'codeParameterForPostRequest' : codeParameterForPostRequest,
                      'oAuthRedirectUri' : redirect_uri,
                      'client_id' : client_id,
                      'client_secret' : client_secret}
    apiURL = httpFunctions.buildFullUrl(apiEndpoint, parameterArray)
    responseDataInJson = httpFunctions.getRequest(apiURL)
    #Convert JSON string to an array
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    #Store data to session
    contextSensitiveFunctions.addOauthSessionVariable(session, 'access_token', responseDataInArray['access_token'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'token_type', responseDataInArray['token_type'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'expires_in', responseDataInArray['expires_in'], 'spotify')
    contextSensitiveFunctions.addOauthSessionVariable(session, 'refresh_token', responseDataInArray['refresh_token'], 'spotify')
