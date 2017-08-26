from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import utils
from flask_admin import Admin
from config import config, Config
from celery import Celery

cel = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND,
                    broker=Config.CELERY_BROKER_URL)
db = SQLAlchemy()
bootstrap = Bootstrap()
admin = Admin(template_mode='bootstrap3')
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
 
    bootstrap.init_app(app)
    db.init_app(app)
    
    mail.init_app(app)

    from app.celery import make_celery
    make_celery(cel, app)

    from app.authService import make_admin
    make_admin(admin, app, db)

    from app.coreService import core
    app.register_blueprint(core)

    from app.classService import repo, configure_up
    app.register_blueprint(repo)
    configure_up(app)

    from app.studentService import progress
    app.register_blueprint(progress)

    from app.reportingService import stats
    app.register_blueprint(stats)

    from app.certService import cert
    app.register_blueprint(cert)

    return app

