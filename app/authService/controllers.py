from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.authService.models import *
from app.authService.forms import *
from sqlalchemy import event
from sqlalchemy import DDL
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
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
        en2 = 'user2@wsu.edu'
        if not user_datastore.get_user(en):
            user_datastore.create_user(email=en, password=encrypted_password, name='Test User')
            user_datastore.add_role_to_user(en, 'end-user')
        if not user_datastore.get_user(ad):
            user_datastore.create_user(email=ad, password=encrypted_password, name='Test Admin')
            user_datastore.add_role_to_user(ad, 'admin')
        if not user_datastore.get_user(en2):
            user_datastore.create_user(email=en2, password=encrypted_password, name='Test User2')
            user_datastore.add_role_to_user(en2, 'end-user')

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
        #from app.reportingService.models import SegmentStats, VideoStats, LectureStats, QuizStats
        #segment = Module(name="Python for Data Analytics", type='segment', parent=uuid.UUID("15909556-081d-42a6-89f1-59ea3aa1116b"), serial=1)
        #db.session.add(segment)
        #db.session.commit()
        #segstats = SegmentStats(module_id=segment.id)
        #db.session.add(segstats)
        #video = Module(name="Introduction to Python/Setup", type='video', parent=segment.id, serial=1)
        #db.session.add(video)
        #db.session.commit()
        #vidstats = VideoStats(module_id=video.id)
        #db.session.add(vidstats)
        #quiz = Module(name="Quiz 1", type='quiz', parent=segment.id, serial=2)
        #db.session.add(quiz)
        #db.session.commit()
        #quizstats = QuizStats(module_id=quiz.id, max_score=50.00)
        #db.session.add(quizstats)
        #cr = [Module(name=names[i-1], author=authors[i-1], type='course', parent=None, serial=i, is_ready=True) for i in range(1,7)]
        #cr[-1].is_ready=False
        #cr[0].children = 2
        #s1 = Module(name='Python for Data Analytics', type='segment', parent=uuid.UUID("e4cbfd4f-ec91-4b7b-8b9f-073d8f5432f0"), serial=1, data={ 'totalModules': 2 })
        #db.session.add(s1)
        #db.session.commit()
        #v1 = Module(name='Introduction to Python', type='video', parent=s1.id, serial=1, data={ 'location': 'pda1' })
        #db.session.add(v1)
        #db.session.commit()
        #q2 = Module(name='Quiz 1', type='quiz', parent=s1.id, serial=2, data={ 'location': '_m3q1' })
        #db.session.add(q2)
        #for c in cr:
        #    db.session.add(c)
        #from app.studentService.models import CourseProgress
        #import uuid
        #cp = CourseProgress(module_id=uuid.UUID('15909556-081d-42a6-89f1-59ea3aa1116b'), user_id=1, completed_segments=1)
        #db.session.add(cp)
        #c = Module(id=uuid.UUID("1d1c8206-4a02-4e4c-8774-59a3b8e93503"),name='Quiz 1', type='quiz', serial=1, parent=uuid.UUID("e4cbfd4f-ec91-4b7b-8b9f-073d8f5432f0"), data={ 'location': '_m3q1' })
        #db.session.add(c)
        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()



