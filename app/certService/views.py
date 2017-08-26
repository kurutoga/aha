from flask import jsonify, session, request
from flask_security import login_required, current_user

from app.classService.controllers import get_module

from . import cert

from .controllers import (
        get_certificate
)
from ..utils import convert_to_uuid, redirect_url, nocache


@cert.route('/user/<user_id>/course/<course_id>')
@login_required
def get_cert(user_id, course_id):
    cert = get_certificate(course_id, user_id)
    course = get_module(course_id)
    d = {}
    d['Course Name']=course.name
    d['Name']=current_user.name
    d['User Email']= current_user.email
    d['Scored Points']=cert.scored_points
    d['Total Points']=cert.total_points
    d['Complated on']=cert.generated_at
    return jsonify([d])


