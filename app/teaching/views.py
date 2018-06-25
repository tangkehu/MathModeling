from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required
from . import teaching
from .tools import baidu_web_search
from ..models import KnowResource


@teaching.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        words = request.form.get("words")
        if words:
            return redirect(url_for('.search', words=words))
        else:
            flash('请输入要查询的内容')
    resource = KnowResource.get_newest()
    return render_template('teaching/main.html', active_flg=['teaching'], resource=resource)


@teaching.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get("words")
        if words:
            return redirect(url_for('.search', words=words))
        else:
            flash('请输入要查询的内容')
    result = baidu_web_search(words)
    resource = KnowResource.search(0, words)
    return render_template('teaching/search.html', active_flg=['teaching'], words=words,
                           baidu_result=result, resource=resource)
