from app import db
from flask_sqlalchemy import declared_attr
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import PrimaryKeyConstraint
from app.utils import _get_now

class ModuleProgressMixin(db.Model):
    __abstract__ = True
    @declared_attr
    def module_id(cls):
        return db.Column('module_id', db.ForeignKey('module.id'), primary_key=True)

    @declared_attr
    def user_id(cls):
        return db.Column('user_id', db.ForeignKey('user.id'), primary_key=True)
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
    __table_args__ = (
            PrimaryKeyConstraint('module_id', 'user_id', name='module_user_lecture_pk'),
            {}
    )


