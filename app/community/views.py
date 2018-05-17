from flask import render_template, request, url_for, redirect
from flask_login import login_required
from . import community


@community.route('/main/<words>', methods=['GET', 'POST'])
@login_required
def main(words):
    if request.method == 'POST':
        new_words = request.form.get('words')
        if new_words:
            words = new_words
        else:
            words = 'null'
        return redirect(url_for('community.main', words=words))
    if request.method == 'GET':
        if words == 'null':
            words = None
        else:
            pass
        return render_template('community/main.html', active_flg=['community'], words=words)


@community.route('/question_add', methods=['GET', 'POST'])
@login_required
def question_add():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('community.main', words='null'))
    return render_template('community/question_add.html', active_flg=['community'])


@community.route('/question_edit/<question_id>', methods=['GET', 'POST'])
@login_required
def question_edit(question_id):
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('community.question_info', question_id=question_id))
    question = question_id
    return render_template('community/question_add.html', active_flg=['community'], question=question)


@community.route('/question_info/<question_id>')
@login_required
def question_info(question_id):
    question = question_id
    return render_template('community/question_info.html', active_flg=['community'], question=question)


@community.route('/answer_add/<question_id>', methods=['GET', 'POST'])
@login_required
def answer_add(question_id):
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('community.question_info', question_id=question_id))
    question = question_id
    return render_template('community/answer_add.html', active_flg=['community'], question=question)


@community.route('/answer_edit/<answer_id>', methods=['GET', 'POST'])
@login_required
def answer_edit(answer_id):
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('community.question_info', question_id=1))
    question = answer_id
    return render_template('community/answer_add.html', active_flg=['community'], question=question, answer=answer_id)

