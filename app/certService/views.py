from flask import jsonify, session, request, send_file
from flask_security import login_required, current_user

from app.classService.controllers import get_module
from config import Config

from . import cert

from .controllers import (
        get_certificate
)
from ..utils import convert_to_uuid, redirect_url, nocache


@cert.route('/user/<user_id>/course/<course_id>')
@login_required
def get_cert(user_id, course_id):
    cert = get_certificate(course_id, user_id)
    return send_file(Config.BASE_PATH+'certs/'+cert.location, attachment_filename='certificate.jpg', as_attachment=True)
