from flask import Blueprint

progress = Blueprint('progress', __name__, url_prefix='/progress')

from . import views
