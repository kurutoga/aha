from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.authService.models import *
from app.authService.forms import *

from app import db, app

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=AHARegisterForm)

#@app.before_first_request
#    user_datastore.create_user(email='bishudash@gmail.com', password='password')
#    db.session.commit()

# Executes before the first request is processed.
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

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

