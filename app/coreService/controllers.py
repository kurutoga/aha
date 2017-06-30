from flask import Blueprint, render_template
from flask_security import login_required, current_user

from app import app, db
from app.authService.controllers import user_datastore
from app.classService.models import Module

core = Blueprint('core', __name__, url_prefix='/')

@core.route('/')
@core.route('dashboard')
def home():
    courses = Module.query.filter_by(type='class').order_by(Module.serial).all()
    progress = {}
    progress["name"]=courses[0].name
    progress["progress"]=25
    progress["id"]=courses[0].id
    if current_user.is_authenticated:
        return render_template('dash.html', courses=courses, available=courses[1:],ongoing=[progress])
    return render_template('home.html')

