#@auth.requires_login()
def index():
    return dict(message=T('Hello World'))
