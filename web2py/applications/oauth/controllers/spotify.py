import customFunctions
import contextSensitiveFunctions
import httpFunctions
def index():
    customFunctions.printToLog('------------------------------------------------')
    customFunctions.printToLog('landingPageSpotify()')
    url = contextSensitiveFunctions.getConfigValue('Spotify','me_endpoint',db)
    authorizationHeader = 'Bearer ' + contextSensitiveFunctions.getOauthSessionVariable(session, 'access_token', 'spotify')
    headers = {'Authorization' : authorizationHeader}
    responseDataInJson = httpFunctions.getRequest(url, None, headers)
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    authorizedUserEmailAddress = responseDataInArray['email']
    return dict(message='Authenticated with Spotify as: ' + authorizedUserEmailAddress)
