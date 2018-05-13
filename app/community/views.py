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


@community.route('/question')
@login_required
def question():
    return 'ok'
