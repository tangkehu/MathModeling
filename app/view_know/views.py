from flask import render_template
from flask_login import login_required
from . import know


@know.route('/push')
@login_required
def push():
    return render_template('know/push.html', active_flg=['know', 'push'])


@know.route('/resource')
@login_required
def resource():
    return render_template('know/resource.html', active_flg=['know', 'resource'])


@know.route('/upload')
@login_required
def upload():
    return render_template('know/upload.html', active_flg=['know', 'resource'])
