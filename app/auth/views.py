# -*- encoding: utf-8 -*-

from flask import render_template, redirect, url_for, request
from flask_login import login_user
from . import auth
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        user = User.query.filter_by(student_id=form_data.get('student_id')).first()
        if user:
            flag = user.check_password(form_data.get('password'))
            if flag:
                if form_data.get('remember'):
                    login_user(user, True)
                else:
                    login_user(user, False)
                return 'true'
            else:
                return u'Tips：学号或密码错误！'
        else:
            return u'Tips：该用户还未注册！'
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        form_data = request.form.to_dict()
        if User.query.filter_by(student_id=form_data.get('student_id')).first():
            return u'Tips：该学号已被注册！'
        else:
            new_user = User()
            form_data['create_time'] = 1
            flag = new_user.edit(form_data)
            if flag:
                return 'true'
            else:
                return u'Tips：注册失败！'

    return redirect(url_for('main.index'))
