from flask import Blueprint

train = Blueprint('train', __name__)

from . import views