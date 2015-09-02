import customFunctions
import httpFunctions
import apiFunctions

@request.restful()
def getConfigValue():
    def GET(resourceOwner, configSetting):
        #Log inputs
        customFunctions.printToLog('getConfigValue GET: resourceOwner: ' + resourceOwner, 0)
        customFunctions.printToLog('getConfigValue GET: configSetting: ' + configSetting, 0)
        #Get the config value
        configVal = apiFunctions.getConfigValueHelper(db, resourceOwner, configSetting)
        #Log the result and return it to the caller
        customFunctions.printToLog('getConfigValue GET: configVal: ' + configVal, 1)
        return configVal
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def adapter_Spotify_me():
    def GET(): 
        return 'abc!'
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)



@request.restful()
def buildUrlToInitiateAuthorization():
    def GET(resourceOwner, oAuthRedirectUri):
        #Fetch this Resource Owner's configuration values
        authorization_endpoint = apiFunctions.getConfigValueHelper(db, resourceOwner, 'authorization_endpoint')
        client_id = apiFunctions.getConfigValueHelper(db, resourceOwner, 'client_id')
        response_type = apiFunctions.getConfigValueHelper(db, resourceOwner, 'response_type')
        scopes = apiFunctions.getConfigValueHelper(db, resourceOwner, 'scopes')
        show_dialog = apiFunctions.getConfigValueHelper(db, resourceOwner, 'show_dialog')
        #Log inputs
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: authorization_endpoint: ' + authorization_endpoint, 0)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: client_id: ' + client_id, 0)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: response_type: ' + response_type, 0)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: scopes: ' + scopes, 0)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: show_dialog: ' + show_dialog, 0)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: oAuthRedirectUri: ' + oAuthRedirectUri, 0)
        #Build the url
        data = {}
        data['client_id'] = client_id
        data['response_type'] = response_type
        data['scope'] = scopes
        data['show_dialog'] = show_dialog
        data['redirect_uri'] = oAuthRedirectUri
        url = httpFunctions.buildFullUrl(authorization_endpoint, data)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: url: ' + oAuthRedirectUri, 1)
        #Return the url to caller
        return url
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def postToTokenEndpointAuthorizationCode():
    def GET(resourceOwner, codeParameterForPostRequest, oAuthRedirectUri):
        #Fetch this Resource Owner's configuration values
        postUrl = apiFunctions.getConfigValueHelper(db, resourceOwner, 'token_endpoint')
        client_id = apiFunctions.getConfigValueHelper(db, resourceOwner, 'client_id')
        client_secret = apiFunctions.getConfigValueHelper(db, resourceOwner, 'client_secret')
        
        #Log inputs
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: postUrl: ' + postUrl, 0)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_id: ' + client_id, 0)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_secret: ' + client_secret, 0)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: codeParameterForPostRequest: ' + codeParameterForPostRequest, 0)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: oAuthRedirectUri: ' + oAuthRedirectUri, 0)
        
        #Call the function to generate the HTTP POST request and receive an array containing the response data from the Resource Owner.
        responseDataInArray = postToTokenEndpointHelper(postUrl, 'authorization_code', codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret)
        
        #Convert the array to a JSON object, log it, and return it to the caller.
        jsonObject = httpFunctions.convertArrayToJson(responseDataInArray)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: jsonObject: ' + jsonObject, 1)
        return jsonObject
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

@request.restful()
def testEndpoint():
    def GET():
        return 'abc!'
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

#Helper function to send an HTTP POST request to the /token endpoint
def postToTokenEndpointHelper(postUrl, grantType, codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret) :
    requestBodyParameters = {'grant_type' : grantType,
                             'code' : codeParameterForPostRequest,
                             'redirect_uri' : oAuthRedirectUri,
                             'client_id' : client_id,
                             'client_secret' : client_secret}
    #Call the function to send the HTTP POST and get the response
    responseFromPost = httpFunctions.postRequest(postUrl, requestBodyParameters)
    #Parse the response and return the data to the caller.
    responseDataInJson = responseFromPost.read()
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    customFunctions.printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray), 1)
    return responseDataInArray
