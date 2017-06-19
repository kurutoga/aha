from flask import Blueprint, render_template
from flask_security import login_required

from app import app, db
from app.authService.controllers import user_datastore

core = Blueprint('core', __name__, url_prefix='/')

@core.route('/')
def home():
    return render_template('home.html')

@core.route('dashboard')
@login_required
def dash():
    return render_template('dash.html')
