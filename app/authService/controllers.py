from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.authService.models import *
from app.authService.forms import *
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

def create_course1(db):
    from app.classService.models import Module, CourseData
    from app.reportingService.models import CourseStats, SegmentStats, VideoStats, LectureStats, QuizStats

    def add_commit(m):
        db.session.add(m)
        db.session.commit()

    course = Module(name="Behavior-Based Data Exploration and Statistical Inference", children=3, \
               author="Dr. Larry Holder, Gina Sprint", is_ready=True, type='course', serial=1)
    add_commit(course)

    courseData = CourseData(id=course.id, 
                            description="Behavior-Based Data Exploration and Statistical Inference is divided into 3 segments. "
                                        "The first segment covers how to use Python for data analytics. This segment illustrates how to setup "
                                        "python, use Jupyter notebook and, utilize powerful tools like numpy, scipy and, pandas for data analytics."
                                        " This is followed by a segment which covers topics on how to work with activity data using Visualization, "
                                        "Aggregation, Time Series and, other methods. Finally, the course ends with a segment on Statistical inference."
                                        " The final segment covers topics on SciKit-Learn, various classification methods, dimensionality reduction and,"
                                        " model evalution.",
                            duration_weeks=12)
    db.session.add(courseData)

    courseStats = CourseStats(module_id=course.id)
    add_commit(courseStats)

    segmentNames = ["Python for Data Analytics", "Working with Activity Data", "Statistical Inference"]
    segmentChildren = [8, 9, 13]
    segmentAuthor = ["Gina Sprint", "Gina Sprint", "Dr. Larry Holder"]

    segments = [Module(name=segmentNames[i], children=segmentChildren[i], author=segmentAuthor[i], is_ready=True, type='segment', serial=i+1, parent=course.id) for i in range(3)]
    for s in segments:
        db.session.add(s)
    db.session.commit()

    for s in segments:
        stat = SegmentStats(module_id=s.id)
        db.session.add(stat)
    db.session.commit()

    modNames = [["Download Slides", "Environment Setup", "Quiz 1", "Jupyter Notebook", "Quiz 2", "Numpy and Scipy: Part 1", "Quiz 3", \
                 "Numpy and Scipy: Part 2", "Quiz 4", "Pandas Series", "Quiz 5", "Pandas Dataframe: Part 1", "Quiz 6", "Pandas Dataframe: Part 2", \
                 "Quiz 7", "Final Quiz"],
                ["Download Slides", "Data Cleaning: Part 1", "Quiz 1", "Data cleaning: Part 2", "Quiz 2", "Hierarchical Indexing", \
                 "Quiz 3", "Visualization", "Quiz 4", "Aggregation", "Quiz 5", "Aggregation Visualization", "Quiz 6", "Time Series", \
                 "Quiz 7", "Time Series Visualization", "Quiz 8", "Final Quiz"],
                ["Download Introduction Slides", "Introduction: Definitions, Data and Methods", "Quiz 1", "Introduction: SciKit-Learn", \
                 "Quiz 2", "Download Classification Methods Slides", "Classification Methods: Nearest Neighbors", \
                 "Quiz 3", "Classification Methods: Naive Bayes", "Quiz 4", "Classification Methods: Decision Trees", \
                 "Quiz 5", "Classification Methods: Neural Networks","Quiz 6", "Classification Methods: Ensemble Methods", \
                 "Quiz 7", "Download Dimensionality Reduction, Clustering Slides", "Dimensionality Reduction, Clustering: Feature Selection", \
                 "Quiz 8", "Dimensionality Clustering: PCA", "Quiz 9", "Dimensionality Reduction, Clustering: Clustering", "Quiz 10", \
                 "Download Model Evaluation Slides", "Model Evaluation: Metrics", "Quiz 11", "Model Evaluation: Cross Validation", "Quiz 12", \
                 "Model Evaluation: Hypothesis Testing", "Quiz 13"]
               ]

    modTypes = [['lecture','video','quiz','video','quiz','video','quiz','video','quiz','video','quiz','video', 'quiz', 'video', 'quiz', 'quiz'],
                ['lecture','video','quiz','video','quiz','video','quiz','video','quiz','video','quiz','video', 'quiz','video','quiz', 'video', 'quiz', 'quiz'],
                ['lecture','video','quiz','vidoe','quiz','lecture','video','quiz','video','quiz','video','quiz','video','quiz','video','quiz',\
                 'lecture','video','quiz','video','quiz','video','quiz','lecture','video','quiz','video','quiz','video','quiz']
               ]

    modLocation = [
                   ['PDA.ppt', 'PDA.v1', 'pdaq1', 'PDA.v2', 'pdaq2','PDA.v3','pdaq3','PDA.v4','pdaq4','PDA.v5','pdaq5', 'PDA.v6', 'pdaq6', \
                    'PDA.v7', 'pdaq7', 'pdaq8' ],
                   ['WAD.ppt', 'WAD.v1', 'wadq1', 'WAD.v2', 'wadq2', 'WAD.v3', 'wadq3','WAD.v4', 'wadq4','WAD.v5', 'wadq5','WAD.v6', 'wadq6',\
                    'WAD.v7','wadq7', 'WAD.v8', 'wadq8', 'wadq9'],
                   ['ml1.pptx', 'ML.v1', 'mlq1', 'ML.v2', 'mlq2', 'ml2.pptx', 'ML.v3', 'mlq3', 'ML.v4', 'mlq4', 'ML.v5', 'mlq5', 'ML.v6', 'mlq6', \
                    'ML.v7', 'mlq7', 'ml3.pptx', 'ML.v8', 'mlq8', 'ML.v9', 'mlq9', 'ML.v10', 'mlq10', 'ml4.pptx', 'ML.v11', 'mlq11', 'ML.v12', \
                    'mlq12', 'ML.v13', 'mlq13']
                  ]

    createdMods = []
    for i,s in enumerate(segments):
        for j in range(len(modNames[i])):
            mod = Module(name=modNames[i][j], type=modTypes[i][j], location=modLocation[i][j], serial=j+1, is_ready=True, parent=s.id, author=segmentAuthor[i])
            db.session.add(mod)
            createdMods.append(mod)
    db.session.commit()
    for cm in createdMods:
        if cm.type=='quiz':
            stat = QuizStats(module_id=cm.id)
        elif cm.type=='video':
            stat = VideoStats(module_id=cm.id)
        else:
            stat = LectureStats(module_id=cm.id)
        db.session.add(stat)
    db.session.commit()

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

        db.session.commit()
        #create_course1(db)
