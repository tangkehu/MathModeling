# -*- encoding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import train


@train.route('/past')
@login_required
def past():
    return render_template('train/past.html', page_title=u'往期集训')
