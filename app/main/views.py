# -*- encoding: utf-8 -*-

from . import main
from flask import render_template, request
from flask_login import login_required, current_user


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        flag = current_user.edit(request.form.to_dict())
        if flag:
            return 'true'
        else:
            return u'修改失败，请重试！'
    else:
        return render_template("user.html", page_title=u'帐号设置')


