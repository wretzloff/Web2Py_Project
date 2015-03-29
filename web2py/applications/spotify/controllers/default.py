#@auth.requires_login()
def index():
    printToLog('------------------------------------------------')
    printToLog('index()')
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    parameterCode = request.vars['code']
    parameterError = request.vars['error']
    if parameterError is not None:
        printToLog('URL parameter \'error\': ' + parameterError)
    elif parameterCode is not None:
        #Generate an HTTP POST to the "token" endpoint and save the results to the session.
        printToLog('URL parameter \'code\': ' + parameterCode)
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
    #url = getConfigValue('spotify_authorization_endpoint')
    #url = 'https://api.spotify.com/v1/search?q=muse&type=artist'
    #getRequest(url, None)
    return dict(message=T('This is the Spotify Landing Page.'))

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
    url = getConfigValue('spotify_authorization_endpoint')
    #Define parameters
    data = {}
    data['client_id'] = getConfigValue('spotify_client_id')
    data['response_type'] = getConfigValue('spotify_response_type')
    data['redirect_uri'] = getConfigValue('spotify_authorization_redirect_uri')
    data['scope'] = getConfigValue('spotify_scopes')
    data['show_dialog'] = getConfigValue('spotify_show_dialog')
    #Build full URL
    full_url = buildFullUrl(url, data)
    return full_url

#Helper function to send an HTTP POST request to the /token endpoint using an OAuth Authorization Code
def postToTokenEndpointAuthorizationCodeSpotify(codeParameterForPostRequest) :
    #Build the HTTP POST payload and then pass it to the function to perform the HTTP POST
    postValues = {'grant_type' : 'authorization_code',
              'code' : codeParameterForPostRequest,
              'redirect_uri' : getConfigValue('spotify_authorization_redirect_uri'),
              'client_id' : getConfigValue('spotify_client_id'),
              'client_secret' : getConfigValue('spotify_client_secret')}
    postToTokenEndpointSpotify(postValues)

#Helper function to send an HTTP POST request to the /token endpoint
def postToTokenEndpointSpotify(requestBodyParameters) :
    import json
    #Get the URL for the /token endpoint
    postUrl = getConfigValue('spotify_token_endpoint')
    #Call the function to send the HTTP POST and get the response
    responseFromPost = postRequest(postUrl, requestBodyParameters)
    #Parse the response and return the data to the caller.
    responseDataInJson = responseFromPost.read()
    responseDataInArray = json.loads(responseDataInJson)
    #Save results to session
    session.access_token = responseDataInArray['access_token']
    session.token_type = responseDataInArray['token_type']
    session.expires_in = responseDataInArray['expires_in']
    session.refresh_token = responseDataInArray['refresh_token']
    printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray))

#Private function to fetch the config value specified by configValue
def getConfigValue(configValue) :
    configValueQueryResults = db(db.config.config_setting == configValue).select()
    configValueFirstResult = configValueQueryResults[0]
    configValue = configValueFirstResult.config_value
    printToLog('getConfigValue: ' + configValue)
    return configValue

def buildFullUrl(path, parametersArray) :
    import urllib
    full_url = path
    if parametersArray is not None:
        url_values = urllib.urlencode(parametersArray)
        full_url = full_url + '?' + url_values
    printToLog('buildFullUrl: ' + full_url)
    return full_url

def printToLog(stringToPrint) :
    print getTimestamp() + '\t' + stringToPrint

def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def getRequest(url, parametersArray) :
    import urllib2
    import urllib
    full_url = buildFullUrl(url, parametersArray)
    #Send GET request and print results
    data = urllib2.urlopen(full_url)
    responseData = data.read()
    printToLog('\t getRequest: ' + responseData)
    return responseData

def postRequest(url, parametersArray) :
    import urllib2
    import urllib
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    printToLog('postRequest: to do: log POST response body here')
    return response
