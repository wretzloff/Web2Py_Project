import customFunctions
import httpFunctions
import apiFunctions

@request.restful()
def callMeEndpoint():
    def GET():
        #Get the URL for Spotify's Me endpoint
        configVal = apiFunctions.getConfigValueHelper(db, 'Spotify', 'me_endpoint')
        
        #2. Send message to endpoint, incouding authorization information.
        #3. Take the response from th endpoint and return it to the caller.
        return 'callMeEndpoint!'
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
