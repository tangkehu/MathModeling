from flask import Blueprint
from flask import render_template
from flask_login import login_required

train = Blueprint('train', __name__)


@train.route('/no_train')
@login_required
def no_train():
    return render_template('train/no_train.html', active_flg=['train'])
