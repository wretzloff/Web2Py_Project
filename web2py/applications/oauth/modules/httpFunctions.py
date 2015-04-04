import customFunctions

def buildFullUrl(path, parametersArray) :
    import urllib
    full_url = path
    if parametersArray is not None:
        url_values = urllib.urlencode(parametersArray)
        full_url = full_url + '?' + url_values
    customFunctions.printToLog('buildFullUrl: ' + full_url)
    return full_url

#Helper function to take in a JSON object and convert it to a normal Python array	
def convertJsonToArray(jsonObject) :
    import json
    customFunctions.printToLog('convertJsonToArray: ' + jsonObject)
    pythonArray = json.loads(jsonObject)
    return pythonArray
	
def postRequest(url, parametersArray, headersArray = None) :
    import urllib2
    import urllib
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    customFunctions.printToLog('postRequest: todo: log POST response body here')
    return response