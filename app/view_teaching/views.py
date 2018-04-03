from flask import render_template
from . import teaching


@teaching.route('/main')
def main():
    return render_template('teaching/main.html', active_flg=['teaching'])
