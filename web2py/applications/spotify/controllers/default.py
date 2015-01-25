#@auth.requires_login()
def index():
    import urllib2
    import urllib
    
    #Define URL
    url = getConfigValue('spotify_authorization_endpoint')
    #Define and encode parameters
    data = {}
    data['client_id'] = getConfigValue('spotify_client_id')
    data['response_type'] = getConfigValue('spotify_response_type')
    data['redirect_uri'] = getConfigValue('spotify_authorization_redirect_uri')
    url_values = urllib.urlencode(data)
    #Build full URL
    full_url = url + '?' + url_values
    #print full_url
    #Send GET request and print results
    #redirect(full_url)
    #data = urllib2.urlopen(full_url)
    #html = data.read()
    #print html
    response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url=full_url)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

#Private function to fetch the config value specified by configValue
def getConfigValue(configValue) :
    redirectQueryResults = db(db.config.config_setting == 'spotify_authorization_redirect_uri').select()
    redirectQueryFirstResult = redirectQueryResults[0]
    redirect_uri = redirectQueryFirstResult.config_value
    return redirect_uri
