from flask import request, redirect, url_for, render_template
from flask_login import login_required
from . import teaching


@teaching.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        return redirect(url_for('.search', search_words=request.form.get("search_words")))
    if request.method == 'GET':
        return render_template('teaching/main.html', active_flg=['teaching'])


@teaching.route('/search/<search_words>', methods=['GET', 'POST'])
@login_required
def search(search_words):
    if request.method == 'POST':
        return redirect(url_for('.search', search_words=request.form.get("search_words")))
    if request.method == 'GET':
        return render_template('teaching/search.html', active_flg=['teaching'], search_words=search_words)
