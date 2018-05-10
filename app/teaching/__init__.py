from flask import Blueprint

teaching = Blueprint('teaching', __name__)

from . import views
