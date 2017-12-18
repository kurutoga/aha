from app import db
import uuid
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from flask_admin.contrib import sqla
from flask_security import current_user
from sqlalchemy import PrimaryKeyConstraint

class Module(db.Model):
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(1024))
    serial = db.Column(db.Integer())
    parent = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'))
    type = db.Column(db.String(50))
    children = db.Column(db.Integer, default=0)
    location = db.Column(db.String(200))
    expires_in = db.Column(db.Integer)
    is_ready = db.Column(db.Boolean)

    parent_ = db.relationship('Module', foreign_keys=[parent], backref="children_", remote_side=[id], lazy=True)
    __table_args__ = (UniqueConstraint('parent', 'serial', name='_parent_serial_uc'),)

    def __str__(self):
        return self.name

class CourseData(db.Model):
    id = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    description     = db.Column(db.Text)
    duration_weeks  = db.Column(db.Integer)
    pass_percent    = db.Column(db.Float, default=70.0)
    video_link       = db.Column(db.String(200))

class  Downloadable(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))

class Prerequisites(db.Model):
    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    prereq_id = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True) 
    __table_args__     = (
            PrimaryKeyConstraint('module_id', 'prereq_id', name='module_prereq_pk'),
            {}
    )

class CourseDataAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    can_delete = False
    can_create = False
    page_size = 50
    column_display_pk = True

class ModuleAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_parent(view, context, model, name):
        return model.parent_

    can_create = False
    can_delete = False
    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'parent': _get_parent
    }

    column_searchable_list = ('id', 'name', 'type', 'serial', 'parent_.name')
    column_sortable_list = ('id','name', 'type', 'serial', 'parent', 'location')
    column_list = ('id', 'type', 'serial', 'name', 'parent', 'author', 'children', 'location', 'expires_in', 'is_ready')
    
