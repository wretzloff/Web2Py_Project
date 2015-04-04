import customFunctions
import httpFunctions

@request.restful()
def testEndpoint():
    def GET():
        return 'returnStringFromTestEndpointGET'
    def POST(*args,**vars):
        #message = 'DEFAULT'
        #target = 'TARGET'
        #if len(args) > 0:
        #    if 'send' == args[0]:
        #        message = args[1]
        #        target = args[2]
        #elif vars['type'] == 'send':
        #    message = vars['message']
        #    target = vars['to']
        return 'returnStringFromTestEndpointPOST'
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

#Helper function to build and return the URL that will be used to initiate the authorization process
@request.restful()
def buildUrlToInitiateAuthorizationSpotify():
    def GET():
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
    def POST(*args,**vars):
        return 'r'
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)
