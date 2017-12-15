from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..classService.controllers import get_courses

class UserEmailForm(FlaskForm):
    email = StringField('Student Email Address', [DataRequired(), Email()])

def _get_user_name_form():
    class UserNameForm(FlaskForm):
        name        = StringField(u'Full Name', validators=[DataRequired("You must provide a name")])
        courses     = QuerySelectField(u'Select Course', query_factory=lambda: get_courses(), get_pk=lambda item: item.id, get_label=lambda item: item.name)
        submit      = SubmitField(u'Create/Update Course')
    return UserNameForm

