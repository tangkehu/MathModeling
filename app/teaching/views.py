from flask import request, redirect, url_for, render_template
from flask_login import login_required
from . import teaching
from .bll import baidu_news_search


@teaching.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        words = request.form.get("words")
        return redirect(url_for('.search', words=words)) if words else redirect(url_for('.main'))
    return render_template('teaching/main.html', active_flg=['teaching'])


@teaching.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get("words")
        return redirect(url_for('.search', words=words)) if words else redirect(url_for('.main'))
    result = baidu_news_search(words)
    return render_template('teaching/search.html', active_flg=['teaching'], words=words, baidu_result=result)
