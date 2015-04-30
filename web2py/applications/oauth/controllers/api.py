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
        #Build the url and return it to the caller
        url = oauthFunctions.buildUrlToInitiateAuthorization(authorization_endpoint,client_id, response_type, oAuthRedirectUri, scopes, show_dialog)
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
        postUrl2 = getConfigValueHelper(resourceOwner, 'token_endpoint')
        client_id2 = getConfigValueHelper(resourceOwner, 'client_id')
        client_secret2 = getConfigValueHelper(resourceOwner, 'client_secret')
        
        #Log inputs
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: postUrl: ' + postUrl2)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: codeParameterForPostRequest: ' + codeParameterForPostRequest)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: oAuthRedirectUri: ' + oAuthRedirectUri)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_id: ' + client_id2)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_secret: ' + client_secret2)
        
        #Call the function to generate the HTTP POST request and receive an array containing the response data from the Resource Owner.
        responseDataInArray = oauthFunctions.postToTokenEndpointAuthorizationCode(postUrl2, codeParameterForPostRequest, oAuthRedirectUri, client_id2, client_secret2)
        
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
