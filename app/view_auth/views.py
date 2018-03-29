from flask import render_template
from . import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/register')
def register():
    return render_template('auth/register.html')


@auth.route('/profile')
def profile():
    return render_template('auth/profile.html')