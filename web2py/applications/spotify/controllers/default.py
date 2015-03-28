#@auth.requires_login()
def index():
    printToLog('------------------------------------------------')
    printToLog('index()')
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    #Generate an HTTP POST to the "token" endpoint.
    parameterCode = request.vars['code']
    parameterError = request.vars['error']
    if parameterError is not None:
        printToLog('URL parameter \'error\': ' + parameterError)
    elif parameterCode is not None:
        printToLog('URL parameter \'code\': ' + parameterCode)
        responseFromPost = sendPostToSpotifyTokenEndpoint(parameterCode)
        session.access_token = responseFromPost['access_token']
        session.token_type = responseFromPost['token_type']
        session.expires_in = responseFromPost['expires_in']
        session.refresh_token = responseFromPost['refresh_token']
        redirect(URL('landingPageSpotify'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = buildUrlToInitiateAuthorizationSpotify()
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)


def landingPageSpotify():
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

#Helper function to send an HTTP POST request to the /token endpoint
def sendPostToSpotifyTokenEndpoint(codeParameterForPostRequest) :
    import json
    postUrl = getConfigValue('spotify_token_endpoint')
    postValues = {'grant_type' : 'authorization_code',
              'code' : codeParameterForPostRequest,
              'redirect_uri' : getConfigValue('spotify_authorization_redirect_uri'),
              'client_id' : getConfigValue('spotify_client_id'),
              'client_secret' : getConfigValue('spotify_client_secret')}
    responseFromPost = postRequest(postUrl, postValues)
    responseDataInJson = responseFromPost.read()
    responseDataInArray = json.loads(responseDataInJson)
    printToLog('sendPostToTokenEndpoint: ' + str(responseDataInArray))
    return responseDataInArray


#Private function to fetch the config value specified by configValue
def getConfigValue(configValue) :
    configValueQueryResults = db(db.config.config_setting == configValue).select()
    configValueFirstResult = configValueQueryResults[0]
    configValue = configValueFirstResult.config_value
    printToLog('getConfigValue: ' + configValue)
    return configValue

def buildFullUrl(path, parametersArray) :
    import urllib
    url_values = urllib.urlencode(parametersArray)
    full_url = path + '?' + url_values
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
