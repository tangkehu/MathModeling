from flask import render_template
from . import know


@know.route('/push')
def push():
    return render_template('know/push.html', active_flg=['know', 'push'])


@know.route('/resource')
def resource():
    return render_template('know/resource.html', active_flg=['know', 'resource'])


@know.route('/upload')
def upload():
    return render_template('know/upload.html', active_flg=['know', 'upload'])
