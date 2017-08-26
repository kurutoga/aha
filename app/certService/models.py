from app import db
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import PrimaryKeyConstraint
from app.utils import _get_now

class Certificate(db.Model):
    course_id        = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    user_id         = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    scored_points   = db.Column(db.Integer())
    total_points    = db.Column(db.Integer())
    generated_at    = db.Column(db.DateTime(), default=_get_now)
    status          = db.Column(db.String(10))
    location        = db.Column(db.String(100))
    __table_args__     = (
            PrimaryKeyConstraint('course_id', 'user_id', name='class_user_cert_pk'),
            {}
    )

