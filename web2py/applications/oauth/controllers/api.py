import customFunctions
import httpFunctions
import oauthFunctions
import contextSensitiveFunctions

@request.restful()
def getConfigValue():
    def GET(resourceOwner, configSetting):
        #Log inputs
        customFunctions.printToLog('getConfigValue GET: resourceOwner: ' + resourceOwner)
        customFunctions.printToLog('getConfigValue GET: configSetting: ' + configSetting)
        #Get the config value
        configVal = getConfigValueHelper(resourceOwner, configSetting)
        #Log the result and return it to the caller
        customFunctions.printToLog('getConfigValue GET: configVal: ' + configVal)
        return configVal
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
        authorization_endpoint = getConfigValueHelper(resourceOwner, 'authorization_endpoint')
        client_id = getConfigValueHelper(resourceOwner, 'client_id')
        response_type = getConfigValueHelper(resourceOwner, 'response_type')
        scopes = getConfigValueHelper(resourceOwner, 'scopes')
        show_dialog = getConfigValueHelper(resourceOwner, 'show_dialog')
        #Log inputs
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: authorization_endpoint: ' + authorization_endpoint)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: client_id: ' + client_id)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: response_type: ' + response_type)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: scopes: ' + scopes)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: show_dialog: ' + show_dialog)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: oAuthRedirectUri: ' + oAuthRedirectUri)
        #Build the url
        data = {}
        data['client_id'] = client_id
        data['response_type'] = response_type
        data['scope'] = scopes
        data['show_dialog'] = show_dialog
        data['redirect_uri'] = oAuthRedirectUri
        url = httpFunctions.buildFullUrl(authorization_endpoint, data)
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
        postUrl = getConfigValueHelper(resourceOwner, 'token_endpoint')
        client_id = getConfigValueHelper(resourceOwner, 'client_id')
        client_secret = getConfigValueHelper(resourceOwner, 'client_secret')
        
        #Log inputs
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: postUrl: ' + postUrl)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_id: ' + client_id)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_secret: ' + client_secret)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: codeParameterForPostRequest: ' + codeParameterForPostRequest)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: oAuthRedirectUri: ' + oAuthRedirectUri)
        
        #Call the function to generate the HTTP POST request and receive an array containing the response data from the Resource Owner.
        responseDataInArray = postToTokenEndpointHelper(postUrl, 'authorization_code', codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret)
        
        #Convert the array to a JSON object, log it, and return it to the caller.
        jsonObject = httpFunctions.convertArrayToJson(responseDataInArray)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: jsonObject: ' + jsonObject)
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

#Helper function to fetch a config value
def getConfigValueHelper(resourceOwner, configSetting):
    if resourceOwner != 'None' :
        resourceOwnerConfigQueryResults = db(db.ResourceOwnerSettings.resourceOwnerName == resourceOwner).select()
        resourceOwnerConfigFirstResult = resourceOwnerConfigQueryResults[0]
        configVal = resourceOwnerConfigFirstResult[configSetting]
    else:
        configValueQueryResults = db(db.config.config_setting == configSetting).select()
        configValueFirstResult = configValueQueryResults[0]
        configVal = configValueFirstResult.config_value
    return configVal

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
    customFunctions.printToLog('postToTokenEndpointSpotify: ' + str(responseDataInArray))
    return responseDataInArray
