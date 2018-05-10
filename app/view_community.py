from flask import Blueprint
from flask import render_template
from flask_login import login_required


community = Blueprint('community', __name__)


@community.route('/main')
@login_required
def main():
    return render_template('community/main.html', active_flg=['community'])
