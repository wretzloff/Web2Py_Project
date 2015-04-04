def test() :
    return 'testtest'

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