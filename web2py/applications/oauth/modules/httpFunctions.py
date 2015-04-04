import customFunctions

def buildFullUrl(path, parametersArray) :
    import urllib
    full_url = path
    if parametersArray is not None:
        url_values = urllib.urlencode(parametersArray)
        full_url = full_url + '?' + url_values
    customFunctions.printToLog('buildFullUrl: ' + full_url)
    return full_url