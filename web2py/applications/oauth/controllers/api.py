import customFunctions
import oauthFunctions

@request.restful()
def buildUrlToInitiateAuthorization():
    def GET(authorization_endpoint,client_id, response_type, oAuthRedirectUri, scopes, show_dialog):
        #Sanitize and log the inputs
        authorization_endpoint = authorization_endpoint or ''
        client_id = client_id or ''
        response_type = response_type or ''
        oAuthRedirectUri = oAuthRedirectUri or ''
        scopes = scopes or ''
        show_dialog = show_dialog or ''
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
