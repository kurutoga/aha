from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from app.authService.models import *
from app.authService.forms import *

from app import db, app

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=AHARegisterForm)

#@app.before_first_request
#def create_user():
#    db.create_all()
#    user_datastore.create_user(email='bishudash@gmail.com', password='password')
#    db.session.commit()
