from app import db
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import PrimaryKeyConstraint
from app.utils import _get_now
from flask_security import current_user
from flask_admin.contrib import sqla
from jinja2 import Markup

class Certificate(db.Model):
    course_id        = db.Column(UUID(as_uuid=True), db.ForeignKey('module.id'), primary_key=True)
    user_id         = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    scored_points   = db.Column(db.Integer())
    total_points    = db.Column(db.Integer())
    generated_at    = db.Column(db.DateTime(), default=_get_now)
    status          = db.Column(db.String(10))
    user            = db.relationship('User', lazy=True)
    module          = db.relationship('Module', lazy=True)

    location        = db.Column(db.String(100))
    __table_args__     = (
            PrimaryKeyConstraint('course_id', 'user_id', name='class_user_cert_pk'),
            {}
    )

class CertificateAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def _get_email(view, context, model, name):
        return model.user.email

    def _get_username(view, context, model, name):
        return model.user.name

    def _get_class(view, context, model, name):
        return model.module.name

    def _get_class_id(view, context, model, name):
        return model.module.id
 
    def _get_link(view, context, model, name):
        return Markup(u"<a href='%s/%s'>%s</a>" % ('/cert/download', str(model.location), 'Download'))

    can_create = False
    can_edit = False
    can_delete = False
    column_auto_select_related = True

    page_size = 50

    # Display primary keys in view
    column_display_pk = True

    column_formatters = {
        'class_id': _get_class_id,
        'email': _get_email,
        'username': _get_username,
        'class': _get_class,
        'download': _get_link
    }

    column_searchable_list = ('user.name', 'user.email', 'module.name', 'module.id')
    column_sortable_list = (('username', 'user.name'), ('email', 'user.email'), 'user_id', ('class', 'module.name'), ('class_id', 'module.id'), 'generated_at')
    column_list = ('class_id', 'class', 'user_id', 'username', 'email', 'scored_points', 'total_points', 'generated_at', 'download')
