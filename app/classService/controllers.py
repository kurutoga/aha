from flask import Blueprint, render_template
from flask_security import login_required, current_user

from app import app, db
from app.classService.models import Module

course = Blueprint('course', __name__, url_prefix='/course')

@course.route('/')
@login_required
def toc(course_id):
    courses = Module.query.filter_by(type='class').order_by(Module.serial).all()
    course = [[c.name, c.id] for c in courses]
    return render_template('course.html', course=course)

#todo: add required field support
#@course.route('/course/<int:courseid>')
#@login_required
#def course(courseid):
#    topics = Module.query.filter_by(type='topic', parent=courseid)
#    topics.sort(key=lambda x: x.serial)
#    topic = []
#    for topic in topics:
#        
