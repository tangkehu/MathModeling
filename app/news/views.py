from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import news
from ..models import News


@news.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        words = request.form.get('words')
        if words:
            return redirect(url_for('.search', words=words))
        flash('请输入关键词')
    news_list = News.get_newest()
    return render_template('news/main.html', active_flg=['news'], news_list=news_list)


@news.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get('words')
        if words:
            return redirect(url_for('.search', words=words))
        flash('请输入关键词')
    news_list = News.search(words)
    return render_template('news/main.html', active_flg=['news'], words=words, news_list=news_list)


@news.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('title') and kwargs.get('content'):
            News.add(kwargs)
            flash('新闻公告添加成功')
            return redirect(url_for('.main'))
        flash('请完善新闻内容')
    return render_template('news/add.html', active_flg=['news'])


@news.route('/info/<news_id>')
@login_required
def info(news_id):
    the_news = News.query.get_or_404(int(news_id))
    the_news.read_count_add()
    return render_template('news/info.html', active_flg=['news'], the_news=the_news)


@news.route('/edit/<news_id>', methods=['GET', 'POST'])
@login_required
def edit(news_id):
    the_news = News.query.get_or_404(int(news_id))
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('title') and kwargs.get('content'):
            the_news.edit(kwargs)
            flash('编辑成功')
            return redirect(url_for('.info', news_id=news_id))
        flash('请完善新闻内容')
    return render_template('news/add.html', active_flg=['news'], the_news=the_news)


@news.route('/delete/<news_id>')
@login_required
def delete(news_id):
    the_news = News.query.get_or_404(int(news_id))
    the_news.delete()
    flash('删除成功')
    return redirect(url_for('.main'))
