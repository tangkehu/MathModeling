from flask import Blueprint

know = Blueprint('know', __name__)

from . import views
