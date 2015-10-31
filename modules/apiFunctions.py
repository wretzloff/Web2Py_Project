#Function to fetch the specified config value using the supplied database connection.
def getConfigValueHelper(db, resourceOwner = None, configSetting = None):
    if resourceOwner != 'None' :
        resourceOwnerConfigQueryResults = db(db.ResourceOwnerSettings.resourceOwnerName == resourceOwner).select()
        resourceOwnerConfigFirstResult = resourceOwnerConfigQueryResults[0]
        configVal = resourceOwnerConfigFirstResult[configSetting]
    else:
        configValueQueryResults = db(db.config.config_setting == configSetting).select()
        configValueFirstResult = configValueQueryResults[0]
        configVal = configValueFirstResult.config_value
    return configVal

