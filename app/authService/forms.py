from flask_security.forms import RegisterForm
from wtforms import TextField, SelectField
from wtforms.validators import Required
import pycountry

class AHARegisterForm(RegisterForm):
    name = TextField('Full Name', [Required()])
    sex = SelectField(u'Sex', choices=[("", "---"), ("M", "Male"), ("F", "Female")])
    city = TextField('City')
    state = TextField('State')
    country = SelectField(u'Country', choices=[(country.alpha_2, country.name) for country in pycountry.countries])
