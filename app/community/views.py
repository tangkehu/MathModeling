from flask import render_template
from flask_login import login_required
from . import community


@community.route('/main')
@login_required
def main():
    return render_template('community/main.html', active_flg=['community'])
