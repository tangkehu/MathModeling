from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required
from . import teaching
from .tools import WebSpider
from ..models import KnowResource


@teaching.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        words = request.form.get("words")
        if words:
            return redirect(url_for('.search', words=words))
        else:
            flash('请输入要查询的内容')
    web_spider = WebSpider('数学建模')
    resource = KnowResource.get_newest()
    return render_template('teaching/main.html', active_flg=['teaching'], resource=resource,
                           web_spider=web_spider.get_baidu())


@teaching.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get("words")
        if words:
            return redirect(url_for('.search', words=words))
        else:
            flash('请输入要查询的内容')
    web_spider = WebSpider(words)
    resource = KnowResource.search(0, words)
    return render_template('teaching/search.html', active_flg=['teaching'], words=words,
                           web_spider=web_spider.get_baidu(), resource=resource)
