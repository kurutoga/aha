from flask import Blueprint

cert = Blueprint('cert', __name__, url_prefix='/cert')

from . import views
