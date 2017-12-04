from app import db
from flask_sqlalchemy import declared_attr
from flask_admin.contrib import sqla
from flask_security import current_user
from flask_admin.contrib import sqla

from ..classService.models import Module

from app.utils import _get_now

class ModuleStatsMixin(db.Model):
    __abstract__ = True
    
    @declared_attr
    def module_id(cls):
        return db.Column('module_id', db.ForeignKey('module.id'), primary_key=True)
    
    @declared_attr
    def module(cls):
        return db.relationship('Module', lazy=True)

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

class StatsAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_parent(view, context, model, name):
        return Module.query.get(model.module.parent)

    can_create = False
    can_edit = False
    can_delete = False
    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'segment': _get_parent
    }

    column_searchable_list = ('module.name',)
    column_sortable_list = ('module',)

class QuizStatsAdmin(StatsAdmin):
    column_list = ('module', 'segment', 'attempts', 'avg_score', 'max_score', 'duration')

class VideoStatsAdmin(StatsAdmin):
    column_list = ('module', 'segment', 'views', 'duration')

class LectureStatsAdmin(StatsAdmin):
    column_list = ('module', 'segment', 'downloads')

class SegmentStatsAdmin(sqla.ModelView): 
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_parent(view, context, model, name):
        return Module.query.get(model.module.parent)
 
    can_create = False
    can_edit = False
    can_delete = False

    column_searchable_list = ('module.name',)
    column_sortable_list = (('module', 'module.name'),)

    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'class': _get_parent
    }


    column_list = ('module', 'class', 'current_students', 'students')

class CourseStatsAdmin(sqla.ModelView): 
    def is_accessible(self):
        return current_user.has_role('admin')

    column_searchable_list = ('module.name',)
    column_sortable_list = (('module', 'module.name'),)

    can_create = False
    can_edit = False
    can_delete = False

    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_list = ('module', 'current_students', 'students')
