#@auth.requires_login()
def index():
    import urllib2
    import urllib
    response.flash = T("Welcome to the Spotify app!")
    #data = {}
    #data['client_id '] = '03281675a01a474ab8c9ecccc0646d82'
    #data['response_type'] = 'code'
    #data['redirect_uri'] = 'https://yahoo.com'
    #url_values = urllib.urlencode(data)
    #print url_values  # The order may differ. name=Somebody+Here&language=Python&location=Northampton
    #url = 'http://www.example.com/example.cgi'
    #full_url = url + '?' + url_values
    #data = urllib2.urlopen(full_url)
    return dict(message=T('Hello World'))


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
