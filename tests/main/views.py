from . import main
from flask import render_template


@main.route('/test')
def test():
    return render_template('test.html')

