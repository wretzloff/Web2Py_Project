import customFunctions
import httpFunctions

@request.restful()
def callMeEndpoint():
    def GET():
        #1. Need to retrieve the URL of the Spotify's Me Endpoint.
            #1a. This is currenty only accessible through the getConfigValue API endpoint.
            #ab. Need to move that functionality into a module, so that it can be accessed from the getConfigValue API endpoint, as well as from here.
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
