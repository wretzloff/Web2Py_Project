#Todo: split functions that need db access into its own module
#Todo: determine which functions can be built into a service instead of function call.
#Todo: convert to use applications\oauth\views\spotify\index instead of applications\oauth\views\default\landingPageSpotify
import customFunctions
import httpFunctions
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
    responseDataInJson = getRequest(url, None, headers)
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
    
#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorizationSpotify() :
    url = customFunctions.getConfigValue('Spotify','authorization_endpoint',db)
    #Define parameters
    data = {}
    data['client_id'] = customFunctions.getConfigValue('Spotify','client_id',db)
    data['response_type'] = customFunctions.getConfigValue('Spotify','response_type',db)
    data['redirect_uri'] = customFunctions.getConfigValue(None,'oAuthRedirectUri',db)
    data['scope'] = customFunctions.getConfigValue('Spotify','scopes',db)
    data['show_dialog'] = customFunctions.getConfigValue('Spotify','show_dialog',db)
    #Build full URL
    full_url = httpFunctions.buildFullUrl(url, data)
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    #Build the HTTP POST payload and then pass it to the function to perform the HTTP POST
    postValues = {'grant_type' : 'authorization_code',
              'code' : codeParameterForPostRequest,
              'redirect_uri' : customFunctions.getConfigValue(None,'oAuthRedirectUri',db),
              'client_id' : customFunctions.getConfigValue('Spotify','client_id',db),
              'client_secret' : customFunctions.getConfigValue('Spotify','client_secret',db)}
    postToTokenEndpointSpotify(postValues)

#Helper function to send an HTTP POST request to the /token endpoint
def postToTokenEndpointSpotify(requestBodyParameters) :
    #Get the URL for the /token endpoint
    postUrl = customFunctions.getConfigValue('Spotify','token_endpoint',db)
    #Call the function to send the HTTP POST and get the response
    responseFromPost = httpFunctions.postRequest(postUrl, requestBodyParameters)
    #Parse the response and return the data to the caller.
    responseDataInJson = responseFromPost.read()
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    #Save results to session
    session.access_token = responseDataInArray['access_token']
    session.token_type = responseDataInArray['token_type']
    session.expires_in = responseDataInArray['expires_in']
    session.refresh_token = responseDataInArray['refresh_token']
    customFunctions.printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray))

def getRequest(url, parametersArray, headersArray = None) :
    import urllib2
    #Build the final URL and the Request object
    full_url = httpFunctions.buildFullUrl(url, parametersArray)
    req = urllib2.Request(full_url)
    #Loop through array of headers and add them to the request headers. 
    #Todo: put this in a function so it can be reused!
    if headersArray is not None:
        for key, value in headersArray.iteritems():
            req.add_header(key,value)
    #Send the request and get the response
    response = urllib2.urlopen(req)
    responseData = response.read()
    customFunctions.printToLog('\t getRequest: ' + responseData)
    
    return responseData
