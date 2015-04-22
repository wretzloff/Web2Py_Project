import oauthFunctions

@request.restful()
def buildUrlToInitiateAuthorization():
    def GET():
        return 'returnStringFrombuildUrlToInitiateAuthorizationGET'
    def POST(*args,**vars):
        return 'returnStringFrombuildUrlToInitiateAuthorizationPOST'
    def PUT(*args,**vars):
        return ''
    def DELETE():
        return ''
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)
