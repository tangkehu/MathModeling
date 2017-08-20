# encoding: utf-8

from flask import render_template
from . import administration


@administration.route('/train')
def train():
    return render_template('adminis/train.html', page_title=u'集训系统管理')


@administration.route('/user')
def user():
    return render_template('adminis/user.html', page_title=u'用户管理')