def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint) :
    print getTimestamp() + '\t' + stringToPrint
	
#Private function to fetch the config value specified by configValue
def getConfigValue(resourceOwner = None, configSetting = None, db = None) :
    if resourceOwner is not None :
        resourceOwnerConfigQueryResults = db(db.ResourceOwnerSettings.resourceOwnerName == resourceOwner).select()
        resourceOwnerConfigFirstResult = resourceOwnerConfigQueryResults[0]
        configValue = resourceOwnerConfigFirstResult[configSetting]
        printToLog('getConfigValue: ' + configValue)
    else:
        configValueQueryResults = db(db.config.config_setting == configSetting).select()
        configValueFirstResult = configValueQueryResults[0]
        configValue = configValueFirstResult.config_value
        printToLog('getConfigValue: ' + configValue)
    return configValue
	
def storeOauthSessionVariable(session, variableType, value, resourceOwner = None) :
	if variableType == 'access_token':
		session[access_token][resourceOwner] = value
	elif variableType == 'token_type':
		session[token_type][resourceOwner] = value
	elif variableType == 'expires_in':
		session[expires_in][resourceOwner] = value
	elif variableType == 'refresh_token':
		session[refresh_token][resourceOwner] = value
	else:
		print 'error'
	