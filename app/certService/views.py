from flask import jsonify, session, request, send_file
from flask_security import login_required, current_user

from app.classService.controllers import get_module
from config import Config

from . import cert

from .controllers import (
        get_certificate, generate_cert
)
from ..utils import convert_to_uuid, redirect_url, nocache, _get_now
from config import Config

BASE_PATH = Config.BASE_PATH

@cert.route('/user/<user_id>/course/<course_id>')
@login_required
def get_cert(user_id, course_id):
    cert = get_certificate(course_id, user_id)
    return send_file(Config.BASE_PATH+'certs/'+cert.location, attachment_filename='certificate.jpg', as_attachment=True)

@cert.route('/generate/<course>/<name>')
@login_required
def send_cert(course, name):
    if not current_user.has_role('admin'):
        return('Unauthorized', 401)
    dt = _get_now().strftime("%m-%d-%Y")
    cert = generate_cert(name, course, dt)
    return send_file(BASE_PATH+'certs/'+cert, attachment_filename='certificate.jpg', as_attachment=True)
