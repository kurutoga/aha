from app import db
from flask_sqlalchemy import declared_attr
from app.utils import _get_now

class ModuleStatsMixin(db.Model):
    __abstract__ = True
    @declared_attr
    def module_id(cls):
        return db.Column('module_id', db.ForeignKey('module.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), default=_get_now)
    modified_at = db.Column(db.DateTime(), onupdate=_get_now)

class CourseStats(ModuleStatsMixin):
    current_students    = db.Column(db.Integer, default=0)
    students            = db.Column(db.Integer, default=0)

class SegmentStats(ModuleStatsMixin):
    current_students    = db.Column(db.Integer, default=0)
    students            = db.Column(db.Integer, default=0)

class QuizStats(ModuleStatsMixin):
    attempts    = db.Column(db.Integer, default=0)
    max_score   = db.Column(db.Float, default=0.0)
    avg_score   = db.Column(db.Float, default=0.0)
    duration    = db.Column(db.BigInteger, default=0)

class VideoStats(ModuleStatsMixin):
    views       = db.Column(db.Integer, default=0)
    duration    = db.Column(db.Float, default=0.0)

class LectureStats(ModuleStatsMixin):
    downloads   = db.Column(db.Integer, default=0)
