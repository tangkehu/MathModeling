from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from urllib.parse import quote, unquote
from . import community
from ..models import CommunityQuestion, CommunityAnswer


@community.route('/main/<words>', methods=['GET', 'POST'])
@login_required
def main(words):
    if request.method == 'POST':
        new_words = request.form.get('words')
        if new_words:
            words = new_words
            return redirect(url_for('community.main', words=quote(words)))
        flash('请输入要搜索的关键词')
    if words == 'null':
        words = None
        result = CommunityQuestion.get_newest()
    else:
        words = unquote(words)
        result = CommunityQuestion.search(words)
    return render_template('community/main.html', active_flg=['community'], words=words, result=result)


@community.route('/question_add/', methods=['GET', 'POST'])
@login_required
def question_add():
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('title'):
            CommunityQuestion.add(kwargs)
            return redirect(url_for('community.main', words='null'))
        flash('请输入问题标题')
    return render_template('community/question_add.html', active_flg=['community'])


@community.route('/question_edit/<question_id>', methods=['GET', 'POST'])
@login_required
def question_edit(question_id):
    the_question = CommunityQuestion.query.get_or_404(int(question_id))
    if not current_user.can('community_manage') and the_question.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('title'):
            the_question.edit(kwargs)
            return redirect(url_for('community.question_info', question_id=question_id))
        flash('请输入问题标题')
    return render_template('community/question_add.html', active_flg=['community'], the_question=the_question)


@community.route('/question_info/<question_id>')
@login_required
def question_info(question_id):
    the_question = CommunityQuestion.query.get_or_404(int(question_id))
    answers = the_question.community_answer.order_by(CommunityAnswer.create_time.desc()).all()
    return render_template('community/question_info.html', active_flg=['community'], the_question=the_question,
                           answers=answers)


@community.route('/question_del/<question_id>')
@login_required
def question_del(question_id):
    the_question = CommunityQuestion.query.get_or_404(int(question_id))
    if not current_user.can('community_manage') and the_question.user_id != current_user.id:
        abort(403)
    the_question.delete()
    flash('删除成功')
    return redirect(url_for('community.main', words='null'))


@community.route('/answer_add/<question_id>', methods=['GET', 'POST'])
@login_required
def answer_add(question_id):
    the_question = CommunityQuestion.query.get_or_404(int(question_id))
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('answer'):
            kwargs['the_question'] = the_question
            CommunityAnswer.add(kwargs)
            return redirect(url_for('community.question_info', question_id=question_id))
        flash('请输入你的答案')
    return render_template('community/answer_add.html', active_flg=['community'], the_question=the_question)


@community.route('/answer_edit/<answer_id>', methods=['GET', 'POST'])
@login_required
def answer_edit(answer_id):
    the_answer = CommunityAnswer.query.get_or_404(int(answer_id))
    if not current_user.can('community_manage') and the_answer.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if kwargs.get('answer'):
            the_answer.edit(kwargs)
            return redirect(url_for('community.question_info', question_id=the_answer.community_question_id))
        flash('请输入你的答案')
    return render_template('community/answer_add.html', active_flg=['community'], the_answer=the_answer,
                           the_question=the_answer.community_question)


@community.route('/answer_del/<answer_id>')
@login_required
def answer_del(answer_id):
    the_answer = CommunityAnswer.query.get_or_404(int(answer_id))
    if not current_user.can('community_manage') and the_answer.user_id != current_user.id:
        abort(403)
    the_question_id = the_answer.community_question_id
    the_answer.delete()
    flash('删除成功')
    return redirect(url_for('.question_info', question_id=the_question_id))
