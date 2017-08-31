from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.authService.forms import *
from app.authService.models import *
from sqlalchemy import event
from sqlalchemy import DDL
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask.ext.security.signals import user_registered
from ..classService.models import *
from ..studentService.models import *
from ..reportingService.models import *
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
    admin.add_view(sqla.ModelView(Module, db.session))
    admin.add_view(MyModelView(CourseData, db.session, list_columns=['id', 'description', 'duration_weeks']))
    admin.add_view(MyModelView(CourseStats, db.session, list_columns=['module_id', 'current_students', 'students', 'created_at', 'modified_at']))    
    admin.add_view(MyModelView(SegmentStats, db.session, list_columns=['module_id', 'current_students', 'students', 'created_at']))
    admin.add_view(MyModelView(LectureStats, db.session, list_columns=['module_id', 'downloads', 'modified_at']))
    admin.add_view(MyModelView(VideoStats, db.session, list_columns=['module_id', 'duration', 'views', 'created_at', 'modified_at']))
    admin.add_view(MyModelView(QuizStats, db.session, list_columns=['module_id', 'max_score', 'avg_score', 'duration', 'attempts', 'created_at', 'modified_at']))
    admin.add_view(MyModelView(CourseProgress, db.session, list_columns=['module_id', 'user_id', 'completed_segments', 'total_points', 'scored_points', 'expires_at', 'is_complete']))
    admin.add_view(MyModelView(SegmentProgress, db.session, list_columns=['module_id', 'user_id', 'completed_segments', 'total_points', 'scored_points', 'is_complete']))
    admin.add_view(MyModelView(QuizProgress, db.session, list_columns=['module_id', 'user_id', 'passing_points', 'awarded_points', 'passing_percent', 'awarded_percent', 'total_points', 'duration', 'is_complete']))
    admin.add_view(MyModelView(LectureProgress, db.session, list_columns=['module_id', 'user_id', 'downloads']))
    admin.add_view(MyModelView(VideoProgress, db.session, list_columns=['module_id', 'user_id', 'duration', 'views']))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))

    from flask_security.signals import user_registered

    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        default_role = user_datastore.find_or_create_role('end-user', description='End user')
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()
