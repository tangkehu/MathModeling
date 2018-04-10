from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from . import auth
from ..forms import LoginForm, RegisterForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('know.push'))
        else:
            flash('密码错误')
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经成功退出帐号')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/register.html', form=form)


@auth.route('/profile')
def profile():
    return render_template('auth/profile.html', active_flg=['profile'])


@auth.route('/account')
def account():
    return render_template('auth/account.html', active_flg=['account'])
