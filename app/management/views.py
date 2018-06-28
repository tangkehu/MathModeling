from flask import render_template
from flask_login import login_required
from . import management
from ..models import FlowCount


@management.route('/main/')
@login_required
def main():
    data = FlowCount.get_echarts_data()
    return render_template('management/main.html', active_flg=['management'], data=data)
