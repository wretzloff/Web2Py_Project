import customFunctions
import httpFunctions
import oauthFunctions

@request.restful()
def buildUrlToInitiateAuthorization():
    def GET(authorization_endpoint,client_id, response_type, oAuthRedirectUri, scopes, show_dialog):
        #Sanitize inputs
        authorization_endpoint = authorization_endpoint or ''
        client_id = client_id or ''
        response_type = response_type or ''
        oAuthRedirectUri = oAuthRedirectUri or ''
        scopes = scopes or ''
        show_dialog = show_dialog or ''
        
        #Log inputs
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: authorization_endpoint: ' + authorization_endpoint)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: client_id: ' + client_id)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: response_type: ' + response_type)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: oAuthRedirectUri: ' + oAuthRedirectUri)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: scopes: ' + scopes)
        customFunctions.printToLog('buildUrlToInitiateAuthorization GET: show_dialog: ' + show_dialog)
        
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
    def GET(postUrl, codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret):
        #Sanitize inputs
        postUrl = postUrl or ''
        codeParameterForPostRequest = codeParameterForPostRequest or ''
        oAuthRedirectUri = oAuthRedirectUri or ''
        client_id = client_id or ''
        client_secret = client_secret or ''
        
        #Log inputs
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: postUrl: ' + postUrl)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: codeParameterForPostRequest: ' + codeParameterForPostRequest)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: oAuthRedirectUri: ' + oAuthRedirectUri)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_id: ' + client_id)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_secret: ' + client_secret)
        
        #Call the function to generate the HTTP POST request and receive an array containing the response data from the Resource Owner.
        responseDataInArray = oauthFunctions.postToTokenEndpointAuthorizationCode(postUrl, codeParameterForPostRequest, oAuthRedirectUri, client_id, client_secret)
        
        #Convert the array to a JSON object, log it, and return it to the caller.
        jsonObject = httpFunctions.convertArrayToJson(responseDataInArray)
        customFunctions.printToLog('postToTokenEndpointAuthorizationCode GET: client_secret: ' + client_secret)
        return jsonObject
    def POST(*args,**vars):
        return ''
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)
