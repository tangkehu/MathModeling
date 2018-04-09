from flask import render_template, redirect, url_for, flash
from . import auth
from ..forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data, form.password.data, form.remember_me.data)
        return redirect(url_for('auth.login'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/login.html', form=form)


@auth.route('/register')
def register():
    return render_template('auth/register.html')


@auth.route('/profile')
def profile():
    return render_template('auth/profile.html', active_flg=['profile'])


@auth.route('/account')
def account():
    return render_template('auth/account.html', active_flg=['account'])
