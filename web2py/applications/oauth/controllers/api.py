import oauthFunctions

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
