from flask import render_template, current_app
from . import main


@main.route('/')
@main.route('/index')
def index():
    current_app.config['PAGE_VIEW'] += 1
    return render_template('index.html')
