from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.authService.forms import *
from app.authService.models import *
from sqlalchemy import event
from sqlalchemy import DDL
from flask import session
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_login import user_logged_out
from flask.ext.security.signals import user_registered
from ..classService.models import *
from ..studentService.models import *
from ..reportingService.models import *
from ..certService.models import *
import uuid

class MyModelView(sqla.ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        # Logic
        return True
def get_user_datastore(db):
    user_datastore = SQLAlchemyDatastore(db, User, Role)
    return user_datastore

def make_admin(admin, app, db):
    admin.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=AHARegisterForm, confirm_register_form=AHAConfirmForm)


    #TODO: refactor into own ViewForms
    # Add Flask-Admin views for Users and Roles
    admin.add_view(ModuleAdmin(Module, db.session))
    admin.add_view(CourseDataAdmin(CourseData, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(CourseStatsAdmin(CourseStats, db.session))
    admin.add_view(SegmentStatsAdmin(SegmentStats, db.session))
    admin.add_view(LectureStatsAdmin(LectureStats, db.session))
    admin.add_view(VideoStatsAdmin(VideoStats, db.session))
    admin.add_view(QuizStatsAdmin(QuizStats, db.session))
    admin.add_view(CourseProgressAdmin(CourseProgress, db.session))
    admin.add_view(SegmentProgressAdmin(SegmentProgress, db.session))
    admin.add_view(LectureProgressAdmin(LectureProgress, db.session))
    admin.add_view(VideoProgressAdmin(VideoProgress, db.session))
    admin.add_view(QuizProgressAdmin(QuizProgress, db.session))
    admin.add_view(QuizMetadataAdmin(QuizMetadata, db.session))
    admin.add_view(CertificateAdmin(Certificate, db.session))

    from flask_security.signals import user_registered

    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        default_role = user_datastore.find_or_create_role('end-user', description='End user')
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()

    @user_logged_out.connect_via(app)
    def user_logout_sighandler(app, user):
        session.pop('_flashes', None)
