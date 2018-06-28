from flask import render_template
from . import main
from ..models import FlowCount


@main.route('/')
@main.route('/index')
def index():
    FlowCount.add_page_view_count()
    return render_template('index.html')
