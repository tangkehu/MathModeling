from . import main


@main.route('/')
@main.route('/index')
def index():
    return '<h1 center>Hello World!</h1>'
