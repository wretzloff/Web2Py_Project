import httpFunctions

#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorization(authorization_endpoint,client_id, response_type, oAuthRedirectUri, scopes,show_dialog) :
    
    #Define parameters
    data = {}
    data['client_id'] = client_id
    data['response_type'] = response_type
    data['redirect_uri'] = oAuthRedirectUri
    data['scope'] = scopes
    data['show_dialog'] = show_dialog
    #Build full URL
    full_url = httpFunctions.buildFullUrl(authorization_endpoint, data)
    return full_url
