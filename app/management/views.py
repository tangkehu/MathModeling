from flask import render_template
from flask_login import login_required
from . import management


@management.route('/main/')
@login_required
def main():
    return render_template('management/main.html', active_flg=['management'])
