from flask_security.forms import RegisterForm
from wtforms import TextField
from wtforms.validators import Required

class AHARegisterForm(RegisterForm):
    name = TextField('Full Name', [Required()])
