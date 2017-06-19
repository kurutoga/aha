from flask import Blueprint, render_template
from flask_security import login_required, current_user

from app import app, db
from app.authService.controllers import user_datastore

core = Blueprint('core', __name__, url_prefix='/')

@core.route('/')
@core.route('dashboard')
def home():
    if current_user.is_authenticated:
        return render_template('dash.html')
    return render_template('home.html')

