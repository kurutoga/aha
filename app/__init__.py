from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_security import utils

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from app.authService.controllers import security, user_datastore
from app.coreService.controllers import core
from app.classService.controllers import course

from app.classService.models import Module

app.register_blueprint(core)
app.register_blueprint(course)
Bootstrap(app)

@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('password')
    en = 'user@wsu.edu'
    ad = 'admin@wsu.edu'
    if not user_datastore.get_user(en):
        user_datastore.create_user(email=en, password=encrypted_password, name='Test User')
        user_datastore.add_role_to_user(en, 'end-user')
    if not user_datastore.get_user(ad):
        user_datastore.create_user(email=ad, password=encrypted_password, name='Test Admin')
        user_datastore.add_role_to_user(ad, 'admin')


    #add courses
    names = ['Behavior data exploration and statistical inference', 
            'Behavior analysis from ambient sensor data',
            'Ambient sensor data from health assessment and intervention',
            'Behavior analysis from mobile sensors',
            'Analysis at scale',
            'Advanced topics in clinical application of behavior sensor data analysis']
    authors = ['Gina Sprint, Dr. Larry Holder',
            'Krista, Dr. Diane Cook',
            'Dr. Maureen Schmitter-Edgecombe, Jessamyn Dahmen',
            'Dr. Larry Holder, Dr. Daine Cook',
            'Dr. Ananth Kalyanaraman',
            'Various']
    cr = [Module(name=names[i-1], author=authors[i-1], modules=i+10, type='class', parent=None, serial=i) for i in range(1,7)]
    for c in cr:
        db.session.add(c)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

