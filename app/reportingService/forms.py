from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class UserEmailForm(FlaskForm):
    email = StringField('Student Email Address', [DataRequired(), Email()])
