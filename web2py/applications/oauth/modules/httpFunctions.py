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
	
#Helper function to take in a normal Python array and convert it to a JSON object
def convertArrayToJson(array) :
	import json
	jsonObject = json.dumps(array)
	customFunctions.printToLog('convertArrayToJson: ' + jsonObject)
	return jsonObject
	
def postRequest(url, parametersArray = None, headersArray = None) :
    import urllib2
    import urllib
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    customFunctions.printToLog('postRequest: todo: log POST response body here')
    return response

def getRequest(url, parametersArray = None, headersArray = None) :
    import urllib2
    #Build the final URL and the Request object
    full_url = buildFullUrl(url, parametersArray)
    req = urllib2.Request(full_url)
    #Loop through array of headers and add them to the request headers. 
    #Todo: put this in a function so it can be reused!
    if headersArray is not None:
        for key, value in headersArray.iteritems():
            req.add_header(key,value)
    #Send the request and get the response
    response = urllib2.urlopen(req)
    responseData = response.read()
    customFunctions.printToLog('\t getRequest: ' + responseData)
    return responseData