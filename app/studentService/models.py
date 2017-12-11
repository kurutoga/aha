import uuid
from app import db
from flask_sqlalchemy import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from flask_admin.contrib import sqla
from flask_security import current_user
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import PrimaryKeyConstraint
from app.utils import _get_now
from ..classService.models import Module

class ModuleProgressMixin(db.Model):
    __abstract__ = True
    @declared_attr
    def module_id(cls):
        return db.Column('module_id', db.ForeignKey('module.id'), primary_key=True)

    @declared_attr
    def user_id(cls):
        return db.Column('user_id', db.ForeignKey('user.id'), primary_key=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)

    @declared_attr
    def module(cls):
        return db.relationship('Module', lazy=True)

    created_at      = db.Column(db.DateTime(), default=_get_now)
    modified_at     = db.Column(db.DateTime(), onupdate=_get_now)
    is_complete     = db.Column(db.Boolean, default=False)
    completed_at    = db.Column(db.DateTime())
    expires_at      = db.Column(db.DateTime())

class CourseProgress(ModuleProgressMixin):
    completed_segments = db.Column(db.Integer())
    total_points       = db.Column(db.Float, default=0.0)
    scored_points      = db.Column(db.Float, default=0.0)
    __table_args__     = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_course_pk'),
            {}
    )

class SegmentProgress(ModuleProgressMixin):
    completed_modules = db.Column(db.Integer())
    total_points      = db.Column(db.Float, default=0.0)
    scored_points     = db.Column(db.Float, default=0.0)
    __table_args__    = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_segment_pk'),
            {}
    )
    
class QuizProgress(ModuleProgressMixin):
    passing_points  = db.Column(db.Float)
    awarded_points  = db.Column(db.Float)
    passing_percent = db.Column(db.Float)
    awarded_percent = db.Column(db.Float)
    total_points    = db.Column(db.Float)
    duration        = db.Column(db.Integer)
    __table_args__  = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_quiz_pk'),
            {}
    )

class VideoProgress(ModuleProgressMixin):
    duration        = db.Column(db.Float)
    views           = db.Column(db.Integer)
    __table_args__  = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_video_pk'),
            {}
    )

class LectureProgress(ModuleProgressMixin):
    downloads       = db.Column(db.Integer)
    __table_args__  = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_lecture_pk'),
            {}
    )

class QuizMetadata(db.Model):
    quiz_id         = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    started         = db.Column(db.Boolean, default=False)
    finished        = db.Column(db.Boolean, default=False)
    quizxmlid       = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz_detailed_result.id'))
    created_at      = db.Column(db.DateTime(), default=_get_now)
    modified_at     = db.Column(db.DateTime(), onupdate=_get_now)
    __table_args__  = (PrimaryKeyConstraint('quiz_id', 'user_id', name='module_user_quizmetadata_pk'),{})

class QuizDetailedResult(db.Model):
    id              = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quizxml         = db.Column(db.Text)
 
class ProgressAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_email(view, context, model, name):
        return model.user.email

    def _get_parent(view, context, model, name):
        return Module.query.get(model.module.parent)

    def _get_username(view, context, model, name):
        return model.user.name

    def _get_mod_id(view, context, model, name):
        return model.module.id

    can_create = False
    can_edit = False
    can_delete = False
    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'id': _get_mod_id,
        'email': _get_email,
        'username': _get_username,
        'segment': _get_parent
    }

    column_searchable_list = ('user.name', 'user.email', 'module.name', 'module.id')
    column_sortable_list = (('username', 'user.name'), ('email', 'user.email'), 'module')

class QuizProgressAdmin(ProgressAdmin):
    column_list = ('id', 'module', 'segment', 'username', 'email', 'passing_points', 'awarded_points', 'total_points', 'duration', 'is_complete')

class VideoProgressAdmin(ProgressAdmin):
    column_list = ('id', 'module', 'segment', 'username', 'email', 'views', 'duration')

class LectureProgressAdmin(ProgressAdmin):
    column_list = ('id', 'module', 'segment', 'username', 'email', 'downloads')

class SegmentProgressAdmin(sqla.ModelView): 
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_email(view, context, model, name):
        return model.user.email

    def _get_parent(view, context, model, name):
        return Module.query.get(model.module.parent)

    def _get_username(view, context, model, name):
        return model.user.name

    def _get_mod_id(view, context, model, name):
        return model.module.id
 
    column_searchable_list = ('user.name', 'user.email', 'module.name', 'module.id')
    column_sortable_list = (('username', 'user.name'), ('email', 'user.email'), 'module')

    can_create = False
    can_edit = False
    can_delete = False

    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'email': _get_email,
        'username': _get_username,
        'class': _get_parent,
        'id': _get_mod_id
    }


    column_list = ('id', 'module', 'class', 'username', 'email', 'completed_modules', 'scored_points', 'total_points')

class CourseProgressAdmin(sqla.ModelView): 
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_email(view, context, model, name):
        return model.user.email

    def _get_username(view, context, model, name):
        return model.user.name

    def _get_mod_id(view, context, model, name):
        return model.module.id
 
    column_searchable_list = ('user.name', 'user.email', 'module.name', 'module.id')
    column_sortable_list = (('username', 'user.name'), ('email', 'user.email'), 'module')

    can_create = False
    can_edit = False
    can_delete = False

    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'id': _get_mod_id,
        'email': _get_email,
        'username': _get_username
    }

    column_list = ('id', 'module', 'username', 'email', 'completed_segments', 'scored_points', 'total_points')
