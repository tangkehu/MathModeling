from . import auth


@auth.route('/login')
def login():
    return '<h1>This is login page.</h1>'
