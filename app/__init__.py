from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from app.authService.controllers import security, user_datastore
from app.coreService.controllers import core

app.register_blueprint(core)
Bootstrap(app)
