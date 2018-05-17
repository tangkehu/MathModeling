from flask import request, redirect, url_for, render_template
from flask_login import login_required
from . import teaching


@teaching.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        return redirect(url_for('.search', words=request.form.get("words")))
    if request.method == 'GET':
        return render_template('teaching/main.html', active_flg=['teaching'])


@teaching.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get("words")
        return redirect(url_for('.search', words=words)) if words else redirect(url_for('.main'))
    if request.method == 'GET':
        return render_template('teaching/search.html', active_flg=['teaching'], words=words)
