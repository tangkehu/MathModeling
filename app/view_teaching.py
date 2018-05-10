from flask import Blueprint
from flask import request, redirect, url_for, render_template
from flask_login import login_required


teaching = Blueprint('teaching', __name__)


@teaching.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for())
    if request.method == 'GET':
        return render_template()
