#Todo: move functions into oauthFunctions module
#Todo: split functions that need db access into its own module
#Todo: service-enable functions in modules.
#Todo: convert to use applications\oauth\views\spotify\index instead of applications\oauth\views\default\landingPageSpotify
import customFunctions
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
    url = customFunctions.getConfigValue('Spotify','me_endpoint',db)
    authorizationHeader = 'Bearer ' + session.access_token
    headers = {'Authorization' : authorizationHeader}
    responseDataInJson = httpFunctions.getRequest(url, None, headers)
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)
    
#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorizationSpotify() :
    url = customFunctions.getConfigValue('Spotify','authorization_endpoint',db)
    client_id = customFunctions.getConfigValue('Spotify','client_id',db)
    response_type = customFunctions.getConfigValue('Spotify','response_type',db)
    redirect_uri = customFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    scope = customFunctions.getConfigValue('Spotify','scopes',db)
    show_dialog = customFunctions.getConfigValue('Spotify','show_dialog',db)
    #Build full URL
    full_url = oauthFunctions.buildUrlToInitiateAuthorization(url, client_id, response_type, redirect_uri, scope, show_dialog)
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    #Build the HTTP POST payload and then pass it to the function to perform the HTTP POST
    postValues = {'grant_type' : 'authorization_code',
              'code' : codeParameterForPostRequest,
              'redirect_uri' : customFunctions.getConfigValue(None,'oAuthRedirectUri',db),
              'client_id' : customFunctions.getConfigValue('Spotify','client_id',db),
              'client_secret' : customFunctions.getConfigValue('Spotify','client_secret',db)}
    postUrl = customFunctions.getConfigValue('Spotify','token_endpoint',db)
    responseDataInArray = oauthFunctions.postToTokenEndpoint(postUrl, postValues)
    session.access_token = responseDataInArray['access_token']
    session.token_type = responseDataInArray['token_type']
    session.expires_in = responseDataInArray['expires_in']
    session.refresh_token = responseDataInArray['refresh_token']


#Helper function to send an HTTP POST request to the /token endpoint
#def postToTokenEndpointSpotify(requestBodyParameters) :
#    #Get the URL for the /token endpoint
#    postUrl = customFunctions.getConfigValue('Spotify','token_endpoint',db)
#    #Call the function to send the HTTP POST and get the response
#    responseFromPost = httpFunctions.postRequest(postUrl, requestBodyParameters)
#    #Parse the response and return the data to the caller.
#    responseDataInJson = responseFromPost.read()
#    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    #Save results to session
#    session.access_token = responseDataInArray['access_token']
    session.token_type = responseDataInArray['token_type']
    session.expires_in = responseDataInArray['expires_in']
    session.refresh_token = responseDataInArray['refresh_token']
    customFunctions.printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray))
