from app import db
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
import uuid

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
    __table_args__ = (UniqueConstraint('parent', 'serial', name='_parent_serial_uc'),)


class CourseData(db.Model):
    id = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer)
    pass_percent = db.Column(db.Float, default=70.0)
