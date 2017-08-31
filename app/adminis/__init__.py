from flask import Blueprint

administration = Blueprint('administration', __name__)

from . import views_train, views_user
