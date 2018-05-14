from flask import render_template, request, redirect, url_for
from flask_login import login_required
from . import news


@news.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        return redirect(url_for('.search', words=request.form.get('words')))
    return render_template('news/main.html', active_flg=['news'])


@news.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        return redirect(url_for('.search', words=request.form.get('words')))
    return render_template('news/main.html', active_flg=['news'], words=words)


@news.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        return redirect(url_for('.main'))
    return render_template('news/add.html', active_flg=['news'])


@news.route('/info/<news_id>')
@login_required
def info(news_id):
    the_news = news_id
    return render_template('news/info.html', active_flg=['news'], the_news=the_news)


@news.route('/edit/<news_id>', methods=['GET', 'POST'])
@login_required
def edit(news_id):
    if request.method == 'POST':
        return redirect(url_for('.info', news_id=news_id))
    the_news = news_id
    return render_template('news/add.html', active_flg=['news'], the_news=the_news)
